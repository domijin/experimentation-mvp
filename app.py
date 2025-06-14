from flask import Flask, render_template, request, make_response
from uuid import uuid4
from products import PRODUCTS

app = Flask(__name__)

@app.route('/')
def home():
    # Get or create user ID
    uid = request.cookies.get('uid') or str(uuid4())
    
    # Create response with cookie
    response = make_response(render_template(
        'home.html',
        products=PRODUCTS
    ))
    
    # Set user ID cookie (2 years expiry)
    response.set_cookie('uid', uid, max_age=63072000)
    
    return response

@app.route('/item/<int:pid>')
def item(pid):
    # Get or create user ID
    uid = request.cookies.get('uid') or str(uuid4())
    
    # Find product
    product = next((p for p in PRODUCTS if p['id'] == pid), None)
    if not product:
        return "Product not found", 404
    
    # Create response with cookie
    response = make_response(render_template(
        'item.html',
        product=product
    ))
    
    # Set user ID cookie (2 years expiry)
    response.set_cookie('uid', uid, max_age=63072000)
    
    return response

@app.route('/<path:path>')
def catch_all(path):
    return "🚧 Not implemented", 501

if __name__ == '__main__':
    app.run(debug=True) 