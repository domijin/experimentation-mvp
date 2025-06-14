from flask import Flask, render_template, request, make_response, g
from uuid import uuid4
from products import PRODUCTS
from growthbook_client import create_growthbook, get_variations
import logging
import uuid

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.before_request
def before_request():
    """
    Create a new GrowthBook instance for each request.
    """
    # Get or create user ID
    g.user_id = request.cookies.get('user_id') or str(uuid4())
    
    # Create GrowthBook instance with user ID
    g.gb = create_growthbook(g.user_id)

@app.after_request
def after_request(response):
    """
    Clean up GrowthBook resources after each request.
    """
    if hasattr(g, 'gb'):
        g.gb.destroy()
    return response

@app.route('/')
def home():
    try:
        # Generate new random user ID on every refresh
        user_id = str(uuid.uuid4())
        logger.info(f"Generated new user ID for home page: {user_id}")

        # Create GrowthBook instance for this request
        gb = create_growthbook(user_id)
        
        # Get variations from GrowthBook
        variations = get_variations(gb, user_id)
        logger.info(f"User {user_id} variations: {variations}")

        # Render template with variations
        return render_template(
            'home.html',
            products=PRODUCTS,
            color=variations['ui_color'],
            link=variations['item_link_behavior']
        )
    except Exception as e:
        logger.error(f"Error in home route: {str(e)}")
        # Fallback to default values
        return render_template(
            'home.html',
            products=PRODUCTS,
            color='light',
            link='same_tab'
        )

@app.route('/item/<int:item_id>')
def item(item_id):
    try:
        # Get or create user ID
        user_id = request.cookies.get('user_id')
        if not user_id:
            user_id = str(uuid.uuid4())
            logger.info(f"Created new user ID: {user_id}")

        # Create GrowthBook instance for this request
        gb = create_growthbook(user_id)
        
        # Get variations from GrowthBook
        variations = get_variations(gb, user_id)
        logger.info(f"User {user_id} variations: {variations}")

        # Get product
        product = next((p for p in PRODUCTS if p['id'] == item_id), None)
        if not product:
            return "Product not found", 404

        # Create response with user ID cookie
        response = make_response(render_template(
            'item.html',
            product=product,
            color=variations['ui_color'],
            link=variations['item_link_behavior']
        ))
        response.set_cookie('user_id', user_id)
        return response
    except Exception as e:
        logger.error(f"Error in item route: {str(e)}")
        # Fallback to default values
        product = next((p for p in PRODUCTS if p['id'] == item_id), None)
        if not product:
            return "Product not found", 404
        return render_template(
            'item.html',
            product=product,
            color='light',
            link='same_tab'
        )

@app.route('/<path:path>')
def catch_all(path):
    return "🚧 Not implemented", 501

if __name__ == '__main__':
    app.run(debug=True) 