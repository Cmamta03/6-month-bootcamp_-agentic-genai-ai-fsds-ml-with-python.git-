import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import uuid

# Page configuration
st.set_page_config(
    page_title="Online Shopping App",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'user' not in st.session_state:
    st.session_state.user = None
if 'orders' not in st.session_state:
    st.session_state.orders = []

# Sample product data
def load_products():
    products = [
        {
            "id": 1,
            "name": "Wireless Bluetooth Headphones",
            "price": 89.99,
            "category": "Electronics",
            "description": "High-quality wireless headphones with noise cancellation",
            "image": "🎧",
            "stock": 50,
            "rating": 4.5
        },
        {
            "id": 2,
            "name": "Smart Fitness Watch",
            "price": 199.99,
            "category": "Electronics",
            "description": "Track your fitness goals with this advanced smartwatch",
            "image": "⌚",
            "stock": 30,
            "rating": 4.8
        },
        {
            "id": 3,
            "name": "Organic Cotton T-Shirt",
            "price": 24.99,
            "category": "Clothing",
            "description": "Comfortable and eco-friendly cotton t-shirt",
            "image": "👕",
            "stock": 100,
            "rating": 4.2
        },
        {
            "id": 4,
            "name": "Running Shoes",
            "price": 129.99,
            "category": "Sports",
            "description": "Professional running shoes for all terrains",
            "image": "👟",
            "stock": 75,
            "rating": 4.6
        },
        {
            "id": 5,
            "name": "Coffee Maker",
            "price": 79.99,
            "category": "Home & Kitchen",
            "description": "Automatic coffee maker with programmable timer",
            "image": "☕",
            "stock": 25,
            "rating": 4.4
        },
        {
            "id": 6,
            "name": "Yoga Mat",
            "price": 34.99,
            "category": "Sports",
            "description": "Non-slip yoga mat for home workouts",
            "image": "🧘",
            "stock": 60,
            "rating": 4.3
        },
        {
            "id": 7,
            "name": "Laptop Stand",
            "price": 45.99,
            "category": "Electronics",
            "description": "Adjustable laptop stand for better ergonomics",
            "image": "💻",
            "stock": 40,
            "rating": 4.1
        },
        {
            "id": 8,
            "name": "Plant Pot Set",
            "price": 29.99,
            "category": "Home & Garden",
            "description": "Beautiful ceramic plant pots for indoor plants",
            "image": "🪴",
            "stock": 35,
            "rating": 4.7
        }
    ]
    return products

# User authentication functions
def register_user(username, email, password):
    users = load_users()
    if username in [user['username'] for user in users]:
        return False, "Username already exists"
    
    new_user = {
        "username": username,
        "email": email,
        "password": password,  # In real app, hash the password
        "created_at": datetime.now().isoformat()
    }
    users.append(new_user)
    save_users(users)
    return True, "Registration successful"

def login_user(username, password):
    users = load_users()
    for user in users:
        if user['username'] == username and user['password'] == password:
            return True, user
    return False, "Invalid credentials"

def load_users():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=2)

# Cart functions
def add_to_cart(product, quantity=1):
    for item in st.session_state.cart:
        if item['product']['id'] == product['id']:
            item['quantity'] += quantity
            return
    st.session_state.cart.append({'product': product, 'quantity': quantity})

def remove_from_cart(product_id):
    st.session_state.cart = [item for item in st.session_state.cart if item['product']['id'] != product_id]

def get_cart_total():
    return sum(item['product']['price'] * item['quantity'] for item in st.session_state.cart)

def get_cart_count():
    return sum(item['quantity'] for item in st.session_state.cart)

# Order functions
def create_order(user, cart_items, shipping_address):
    order = {
        "id": str(uuid.uuid4()),
        "user": user,
        "items": cart_items,
        "total": get_cart_total(),
        "shipping_address": shipping_address,
        "status": "Pending",
        "created_at": datetime.now().isoformat()
    }
    st.session_state.orders.append(order)
    st.session_state.cart = []
    return order

# Main application
def main():
    st.title("🛒 Online Shopping App")
    
    # Sidebar for navigation and user actions
    with st.sidebar:
        st.header("Navigation")
        page = st.selectbox(
            "Choose a page",
            ["Home", "Products", "Cart", "Orders", "Account"]
        )
        
        # User authentication section
        st.header("Account")
        if st.session_state.user is None:
            tab1, tab2 = st.tabs(["Login", "Register"])
            
            with tab1:
                st.subheader("Login")
                login_username = st.text_input("Username", key="login_username")
                login_password = st.text_input("Password", type="password", key="login_password")
                
                if st.button("Login"):
                    success, result = login_user(login_username, login_password)
                    if success:
                        st.session_state.user = result
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error(result)
            
            with tab2:
                st.subheader("Register")
                reg_username = st.text_input("Username", key="reg_username")
                reg_email = st.text_input("Email", key="reg_email")
                reg_password = st.text_input("Password", type="password", key="reg_password")
                
                if st.button("Register"):
                    success, message = register_user(reg_username, reg_email, reg_password)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
        else:
            st.success(f"Welcome, {st.session_state.user['username']}!")
            if st.button("Logout"):
                st.session_state.user = None
                st.rerun()
        
        # Cart summary
        if st.session_state.cart:
            st.header("Cart Summary")
            st.write(f"Items: {get_cart_count()}")
            st.write(f"Total: ${get_cart_total():.2f}")
    
    # Main content area
    if page == "Home":
        show_home_page()
    elif page == "Products":
        show_products_page()
    elif page == "Cart":
        show_cart_page()
    elif page == "Orders":
        show_orders_page()
    elif page == "Account":
        show_account_page()

def show_home_page():
    st.header("Welcome to Our Online Store! 🛍️")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Discover Amazing Products
        
        We offer a wide range of high-quality products at competitive prices:
        - 🎧 **Electronics**: Latest gadgets and accessories
        - 👕 **Clothing**: Fashionable and comfortable apparel
        - 🏃 **Sports**: Equipment for your active lifestyle
        - 🏠 **Home & Kitchen**: Everything for your home
        
        ### Why Choose Us?
        - ✅ Free shipping on orders over $50
        - ✅ 30-day return policy
        - ✅ Secure payment processing
        - ✅ 24/7 customer support
        """)
    
    with col2:
        st.markdown("### Quick Stats")
        products = load_products()
        categories = set(product['category'] for product in products)
        
        st.metric("Total Products", len(products))
        st.metric("Categories", len(categories))
        st.metric("Avg Rating", "4.5 ⭐")
        
        if st.session_state.cart:
            st.metric("Cart Items", get_cart_count())
            st.metric("Cart Total", f"${get_cart_total():.2f}")

def show_products_page():
    st.header("🛍️ Product Catalog")
    
    products = load_products()
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        categories = ["All"] + list(set(product['category'] for product in products))
        selected_category = st.selectbox("Category", categories)
    
    with col2:
        price_range = st.slider("Price Range", 0, 300, (0, 300))
    
    with col3:
        min_rating = st.slider("Minimum Rating", 0.0, 5.0, 0.0, 0.1)
    
    # Filter products
    filtered_products = products
    if selected_category != "All":
        filtered_products = [p for p in filtered_products if p['category'] == selected_category]
    
    filtered_products = [p for p in filtered_products if price_range[0] <= p['price'] <= price_range[1]]
    filtered_products = [p for p in filtered_products if p['rating'] >= min_rating]
    
    # Display products in a grid
    cols = st.columns(4)
    for i, product in enumerate(filtered_products):
        with cols[i % 4]:
            st.markdown(f"### {product['image']} {product['name']}")
            st.write(f"**${product['price']:.2f}**")
            st.write(f"Rating: {'⭐' * int(product['rating'])} ({product['rating']})")
            st.write(f"Category: {product['category']}")
            st.write(product['description'][:50] + "...")
            st.write(f"Stock: {product['stock']} units")
            
            col1, col2 = st.columns(2)
            with col1:
                quantity = st.number_input("Qty", min_value=1, max_value=product['stock'], value=1, key=f"qty_{product['id']}")
            with col2:
                if st.button("Add to Cart", key=f"add_{product['id']}"):
                    add_to_cart(product, quantity)
                    st.success(f"Added {quantity} {product['name']} to cart!")
        
        if (i + 1) % 4 == 0:
            st.markdown("---")

def show_cart_page():
    st.header("🛒 Shopping Cart")
    
    if not st.session_state.cart:
        st.info("Your cart is empty. Add some products!")
        return
    
    # Display cart items
    for i, item in enumerate(st.session_state.cart):
        col1, col2, col3, col4, col5 = st.columns([1, 3, 1, 1, 1])
        
        with col1:
            st.write(item['product']['image'])
        
        with col2:
            st.write(f"**{item['product']['name']}**")
            st.write(f"Price: ${item['product']['price']:.2f}")
        
        with col3:
            st.write(f"Qty: {item['quantity']}")
        
        with col4:
            st.write(f"${item['product']['price'] * item['quantity']:.2f}")
        
        with col5:
            if st.button("Remove", key=f"remove_{i}"):
                remove_from_cart(item['product']['id'])
                st.rerun()
    
    st.markdown("---")
    
    # Cart summary and checkout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Cart Summary")
        st.write(f"Total Items: {get_cart_count()}")
        st.write(f"Subtotal: ${get_cart_total():.2f}")
        shipping = 0 if get_cart_total() > 50 else 5.99
        st.write(f"Shipping: ${shipping:.2f}")
        st.write(f"**Total: ${get_cart_total() + shipping:.2f}**")
    
    with col2:
        st.subheader("Checkout")
        if st.session_state.user is None:
            st.warning("Please login to checkout")
        else:
            shipping_address = st.text_area("Shipping Address", height=100)
            if st.button("Place Order"):
                if shipping_address.strip():
                    order = create_order(st.session_state.user, st.session_state.cart, shipping_address)
                    st.success(f"Order placed successfully! Order ID: {order['id']}")
                    st.rerun()
                else:
                    st.error("Please enter a shipping address")

def show_orders_page():
    st.header("📦 My Orders")
    
    if st.session_state.user is None:
        st.warning("Please login to view orders")
        return
    
    user_orders = [order for order in st.session_state.orders if order['user']['username'] == st.session_state.user['username']]
    
    if not user_orders:
        st.info("No orders found. Start shopping!")
        return
    
    for order in user_orders:
        with st.expander(f"Order {order['id'][:8]} - {order['status']} - ${order['total']:.2f}"):
            st.write(f"**Date:** {order['created_at'][:10]}")
            st.write(f"**Status:** {order['status']}")
            st.write(f"**Total:** ${order['total']:.2f}")
            st.write(f"**Shipping Address:** {order['shipping_address']}")
            
            st.subheader("Items:")
            for item in order['items']:
                st.write(f"- {item['product']['name']} x{item['quantity']} = ${item['product']['price'] * item['quantity']:.2f}")

def show_account_page():
    st.header("👤 Account Settings")
    
    if st.session_state.user is None:
        st.warning("Please login to view account settings")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Profile Information")
        st.write(f"**Username:** {st.session_state.user['username']}")
        st.write(f"**Email:** {st.session_state.user['email']}")
        st.write(f"**Member since:** {st.session_state.user['created_at'][:10]}")
    
    with col2:
        st.subheader("Account Statistics")
        user_orders = [order for order in st.session_state.orders if order['user']['username'] == st.session_state.user['username']]
        total_spent = sum(order['total'] for order in user_orders)
        
        st.metric("Total Orders", len(user_orders))
        st.metric("Total Spent", f"${total_spent:.2f}")
        st.metric("Current Cart Items", get_cart_count())

if __name__ == "__main__":
    main() 