from flask import Flask, render_template, request, make_response, g
from uuid import uuid4
from products import PRODUCTS
from growthbook_client import create_growthbook, get_variations
import logging

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
    g.user_id = request.cookies.get('uid') or str(uuid4())
    
    # Create GrowthBook instance
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
        # Get feature flag variations
        variations = get_variations(g.gb)
    except Exception as e:
        logger.error(f"Error in home route: {str(e)}")
        # Fallback to default variations
        variations = {
            'ui_color': 'light',
            'item_link_behavior': 'same_tab'
        }
    
    # Create response with cookie
    response = make_response(render_template(
        'home.html',
        products=PRODUCTS,
        color=variations['ui_color'],
        link=variations['item_link_behavior']
    ))
    
    # Set user ID cookie (2 years expiry)
    response.set_cookie('uid', g.user_id, max_age=63072000)
    
    return response

@app.route('/item/<int:pid>')
def item(pid):
    # Find product
    product = next((p for p in PRODUCTS if p['id'] == pid), None)
    if not product:
        return "Product not found", 404
    
    try:
        # Get feature flag variations
        variations = get_variations(g.gb)
    except Exception as e:
        logger.error(f"Error in item route: {str(e)}")
        # Fallback to default variations
        variations = {
            'ui_color': 'light',
            'item_link_behavior': 'same_tab'
        }
    
    # Create response with cookie
    response = make_response(render_template(
        'item.html',
        product=product,
        color=variations['ui_color'],
        link=variations['item_link_behavior']
    ))
    
    # Set user ID cookie (2 years expiry)
    response.set_cookie('uid', g.user_id, max_age=63072000)
    
    return response

@app.route('/<path:path>')
def catch_all(path):
    return "🚧 Not implemented", 501

if __name__ == '__main__':
    app.run(debug=True) 