"""
app.py
Smart Search Online Store - Main Application Server

Subject Integrations:
1. ADSA (Advanced Data Structures & Algorithms):
   - AVL Tree index of all 5,000+ products for O(log N) lookup and prefix autocomplete.
   - Calculates and returns real search execution time in milliseconds.
2. DMGT (Discrete Mathematics & Graph Theory):
   - Set operations (Intersection ∩, Union ∪, Universe U) for multi-dimensional filtering.
   - Generates exact mathematical set formulas for active filters.
3. OOP (Object-Oriented Programming):
   - Encapsulated classes for Product, CartItem, Cart, Customer, OrderItem, Order, SearchEngine.
4. Python:
   - TF-IDF Cosine Similarity for dynamic product description recommendations.
"""

import csv
import json
import os
import time
from datetime import datetime
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from avl_tree import AVLTree
from recommender import ProductRecommender

# Initialize Flask application
app = Flask(__name__, static_folder=".")
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "products.csv")
ORDERS_FILE = os.path.join(BASE_DIR, "orders.json")

# ==============================================================================
# OOP DOMAIN MODEL
# ==============================================================================

class Product:
    """Represents a product item in the catalog."""
    def __init__(self, p_id, name, category, brand, price, rating, stock, description, image, keywords=""):
        self.id = str(p_id).strip()
        self.name = str(name).strip()
        self.category = str(category).strip()
        self.brand = str(brand).strip()
        self.price = float(price)
        self.rating = float(rating)
        self.stock = int(stock)
        self.description = str(description).strip()
        self.image = str(image).strip()
        self.keywords = str(keywords).strip()

    def in_stock(self):
        return self.stock > 0

    def to_dict(self):
        return {
            "ID": self.id,
            "Name": self.name,
            "Category": self.category,
            "Brand": self.brand,
            "Price": self.price,
            "Rating": self.rating,
            "Stock": self.stock,
            "Description": self.description,
            "Image": self.image,
            "Keywords": self.keywords,
            "InStock": self.in_stock()
        }

class Customer:
    """Represents a store customer."""
    def __init__(self, name, phone, email, address, city, state, pincode):
        self.name = name.strip()
        self.phone = phone.strip()
        self.email = email.strip()
        self.address = address.strip()
        self.city = city.strip()
        self.state = state.strip()
        self.pincode = pincode.strip()

    def to_dict(self):
        return {
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "pincode": self.pincode
        }

class OrderItem:
    """Represents an individual line item in an order."""
    def __init__(self, product_id, product_name, price, quantity):
        self.product_id = product_id
        self.product_name = product_name
        self.price = float(price)
        self.quantity = int(quantity)
        self.subtotal = self.price * self.quantity

    def to_dict(self):
        return {
            "productId": self.product_id,
            "productName": self.product_name,
            "price": self.price,
            "quantity": self.quantity,
            "subtotal": self.subtotal
        }

class Order:
    """Encapsulates an order entity."""
    _counter = 1000

    def __init__(self, customer, items, total_amount, payment_method, status="Confirmed", order_id=None, date_str=None):
        if order_id:
            self.order_id = order_id
        else:
            Order._counter += 1
            self.order_id = f"ORD-{Order._counter}"
        self.customer = customer
        self.items = items  # list of OrderItem
        self.total_amount = float(total_amount)
        self.payment_method = payment_method
        self.status = status
        self.order_date = date_str or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "orderId": self.order_id,
            "customer": self.customer.to_dict() if isinstance(self.customer, Customer) else self.customer,
            "items": [item.to_dict() if isinstance(item, OrderItem) else item for item in self.items],
            "totalAmount": self.total_amount,
            "paymentMethod": self.payment_method,
            "status": self.status,
            "orderDate": self.order_date
        }

# ==============================================================================
# DMGT FILTER ENGINE (Discrete Mathematics Set Operations)
# ==============================================================================

class DMGTFilterEngine:
    """
    Implements Discrete Mathematics and Graph Theory (DMGT) Set Theory
    for multi-attribute product filtering.
    
    Mathematical Foundations:
    - Universe: U = { all products }
    - Category Sets: S_cat(c) = { p in U | p.Category == c }
    - Brand Sets: S_brand(b) = { p in U | p.Brand == b }
    - Price Set: S_price = { p in U | min_p <= p.Price <= max_p }
    - Rating Set: S_rating = { p in U | p.Rating >= min_r }
    - Stock Set: S_stock = { p in U | p.Stock > 0 }
    
    Formula:
    S_result = (⋃ S_cat) ∩ (⋃ S_brand) ∩ S_price ∩ S_rating ∩ S_stock
    """
    def __init__(self, products):
        self.products = products
        self.product_map = {p.id: p for p in products}
        self.universe = set(p.id for p in products)
        
        # Build category sets
        self.category_sets = {}
        for p in products:
            if p.category not in self.category_sets:
                self.category_sets[p.category] = set()
            self.category_sets[p.category].add(p.id)
            
        # Build brand sets
        self.brand_sets = {}
        for p in products:
            if p.brand not in self.brand_sets:
                self.brand_sets[p.brand] = set()
            self.brand_sets[p.brand].add(p.id)

    def filter_products(self, categories=None, brands=None, min_price=None, max_price=None, min_rating=None, in_stock_only=False):
        start_time = time.perf_counter()
        formula_parts = []

        # 1. Category Set (Union over chosen categories)
        if categories:
            cat_list = [c.strip() for c in categories if c.strip()]
            if cat_list:
                cat_union = set()
                for c in cat_list:
                    cat_union |= self.category_sets.get(c, set())
                formula_parts.append(f"({' ∪ '.join(cat_list)})")
            else:
                cat_union = self.universe
        else:
            cat_union = self.universe

        # 2. Brand Set (Union over chosen brands)
        if brands:
            brand_list = [b.strip() for b in brands if b.strip()]
            if brand_list:
                brand_union = set()
                for b in brand_list:
                    brand_union |= self.brand_sets.get(b, set())
                formula_parts.append(f"({' ∪ '.join(brand_list)})")
            else:
                brand_union = self.universe
        else:
            brand_union = self.universe

        # 3. Price Set
        price_conditions = []
        if min_price is not None:
            min_p = float(min_price)
            price_conditions.append(f"Price ≥ ₹{int(min_p)}")
        else:
            min_p = 0.0

        if max_price is not None:
            max_p = float(max_price)
            price_conditions.append(f"Price ≤ ₹{int(max_p)}")
        else:
            max_p = float("inf")

        if price_conditions:
            price_set = {p.id for p in self.products if min_p <= p.price <= max_p}
            formula_parts.append(f"({' and '.join(price_conditions)})")
        else:
            price_set = self.universe

        # 4. Rating Set
        if min_rating is not None and float(min_rating) > 0:
            min_r = float(min_rating)
            rating_set = {p.id for p in self.products if p.rating >= min_r}
            formula_parts.append(f"(Rating ≥ {min_r}★)")
        else:
            rating_set = self.universe

        # 5. Availability Set
        if in_stock_only:
            stock_set = {p.id for p in self.products if p.stock > 0}
            formula_parts.append("(Stock > 0)")
        else:
            stock_set = self.universe

        # DMGT Intersection: S_result = S_cat ∩ S_brand ∩ S_price ∩ S_rating ∩ S_stock
        result_ids = cat_union & brand_union & price_set & rating_set & stock_set

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        formula_str = " ∩ ".join(formula_parts) if formula_parts else "Universe (U)"
        math_expression = f"S_result = {formula_str}"

        return {
            "matching_ids": list(result_ids),
            "count": len(result_ids),
            "math_formula": math_expression,
            "filter_time_ms": round(elapsed_ms, 4),
            "operation": "DMGT Set Intersection (∩) and Union (∪)",
            "universe_size": len(self.universe)
        }

# ==============================================================================
# STORE ENGINE (SYSTEM CONTROLLER)
# ==============================================================================

class StoreEngine:
    """Coordinates AVL Tree, DMGT Set Filter, Cosine Recommender and Orders."""
    def __init__(self):
        self.products = []
        self.product_map = {}
        self.avl_tree = AVLTree()
        self.recommender = None
        self.filter_engine = None
        self.orders = []
        self._load_products()
        self._build_avl_index()
        self._init_recommender()
        self._load_orders()

    def _load_products(self):
        print(f"[StoreEngine] Loading products from {CSV_FILE}...")
        if not os.path.exists(CSV_FILE):
            print("[StoreEngine] Warning: products.csv not found. Running generate_data...")
            import generate_data
            generate_data.main()

        with open(CSV_FILE, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                prod = Product(
                    p_id=row["ID"],
                    name=row["Name"],
                    category=row["Category"],
                    brand=row["Brand"],
                    price=row["Price"],
                    rating=row["Rating"],
                    stock=row["Stock"],
                    description=row["Description"],
                    image=row["Image"],
                    keywords=row.get("Keywords", "")
                )
                self.products.append(prod)
                self.product_map[prod.id] = prod

        print(f"[StoreEngine] Successfully loaded {len(self.products)} products.")
        self.filter_engine = DMGTFilterEngine(self.products)

    def _build_avl_index(self):
        print("[StoreEngine] Indexing products into Self-Balancing AVL Tree...")
        start_time = time.perf_counter()
        
        # Key categories and generic search keywords to prioritize in autocomplete
        common_terms = [
            "Laptop", "Laptop Stand", "Laptop Charger", "Gaming Laptop", "Laptop Bag",
            "Smartphone", "Android Phone", "iPhone", "5G Mobile",
            "Tablet", "iPad", "Digital Notepad", "Stylus Tablet",
            "Headphones", "Wireless Headphones", "Noise Cancelling Headphones",
            "Earbuds", "AirPods", "True Wireless Earbuds",
            "Smart Watch", "Fitness Tracker", "Running Watch",
            "Monitor", "Gaming Monitor", "4K Monitor", "Ultrawide Monitor",
            "Keyboard", "Mechanical Keyboard", "Wireless Keyboard",
            "Mouse", "Gaming Mouse", "Wireless Mouse", "Ergonomic Mouse",
            "Camera", "Mirrorless Camera", "Action Camera", "4K Camera",
            "TV", "Smart TV", "4K TV", "OLED TV",
            "Speaker", "Bluetooth Speaker", "Party Speaker",
            "Charger", "Fast Charger", "GaN Charger", "Type-C Charger",
            "Power Bank", "Portable Charger", "10000mAh Power Bank", "20000mAh Power Bank",
            "Accessories", "USB-C Hub", "Docking Station", "HDMI Cable"
        ]
        
        for term in common_terms:
            self.avl_tree.insert(term, None)

        for p in self.products:
            # 1. Full product name
            self.avl_tree.insert(p.name, p.id)
            # 2. Category name
            self.avl_tree.insert(p.category, p.id)
            # 3. Brand name
            self.avl_tree.insert(p.brand, p.id)
            # 4. Brand + Category (e.g. "Apple Laptop", "Dell Laptop")
            self.avl_tree.insert(f"{p.brand} {p.category}", p.id)
            
            # 5. Token prefixes from product name
            tokens = p.name.split()
            for i in range(1, min(len(tokens) + 1, 4)):
                phrase = " ".join(tokens[:i])
                self.avl_tree.insert(phrase, p.id)

        elapsed = time.perf_counter() - start_time
        stats = self.avl_tree.get_stats()
        print(f"[StoreEngine] AVL Tree built in {elapsed:.3f}s. Height: {stats['height']}, Nodes: {stats['total_nodes']}, Balanced: {stats['is_balanced']}")

    def _init_recommender(self):
        print("[StoreEngine] Initializing Cosine Similarity Recommender...")
        prod_dicts = [p.to_dict() for p in self.products]
        self.recommender = ProductRecommender(prod_dicts)
        print("[StoreEngine] Recommender initialized successfully.")

    def _load_orders(self):
        if os.path.exists(ORDERS_FILE):
            try:
                with open(ORDERS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.orders = data
                    # Update order counter
                    max_num = 1000
                    for ord_dict in self.orders:
                        oid = ord_dict.get("orderId", "")
                        if oid.startswith("ORD-"):
                            try:
                                num = int(oid.split("-")[1])
                                if num > max_num:
                                    max_num = num
                            except ValueError:
                                pass
                    Order._counter = max_num
            except Exception as e:
                print(f"[StoreEngine] Error reading orders.json: {e}")
                self.orders = []
        else:
            # Seed initial sample order for My Orders demo
            sample_order = {
                "orderId": "ORD-1001",
                "customer": {
                    "name": "Alex Johnson",
                    "phone": "+91 98765 43210",
                    "email": "alex.johnson@example.com",
                    "address": "42 Tech Boulevard, Silicon Park",
                    "city": "Bengaluru",
                    "state": "Karnataka",
                    "pincode": "560100"
                },
                "items": [
                    {
                        "productId": "PROD-1001",
                        "productName": "Dell ProBook 450 Creator Series - Rose Gold",
                        "price": 173700,
                        "quantity": 1,
                        "subtotal": 173700
                    }
                ],
                "totalAmount": 173700,
                "paymentMethod": "Demo Cash on Delivery",
                "status": "Confirmed",
                "orderDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.orders = [sample_order]
            self._save_orders()

    def _save_orders(self):
        try:
            with open(ORDERS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.orders, f, indent=2)
        except Exception as e:
            print(f"[StoreEngine] Error saving orders: {e}")

    def add_order(self, order_data):
        cust_data = order_data.get("customer", {})
        customer = Customer(
            name=cust_data.get("name", "Guest"),
            phone=cust_data.get("phone", ""),
            email=cust_data.get("email", ""),
            address=cust_data.get("address", ""),
            city=cust_data.get("city", ""),
            state=cust_data.get("state", ""),
            pincode=cust_data.get("pincode", "")
        )
        
        items = []
        for itm in order_data.get("items", []):
            items.append(OrderItem(
                product_id=itm.get("productId", ""),
                product_name=itm.get("productName", ""),
                price=itm.get("price", 0),
                quantity=itm.get("quantity", 1)
            ))
            
        order = Order(
            customer=customer,
            items=items,
            total_amount=order_data.get("totalAmount", 0),
            payment_method=order_data.get("paymentMethod", "Demo Cash on Delivery"),
            status="Confirmed"
        )
        
        order_dict = order.to_dict()
        self.orders.insert(0, order_dict) # newest first
        self._save_orders()
        return order_dict

# Instantiate Singleton Store Engine
store = StoreEngine()

# ==============================================================================
# STATIC & HTML ROUTES
# ==============================================================================

@app.route("/")
def index_page():
    return send_from_directory(".", "index.html")

@app.route("/<path:path>")
def static_files(path):
    # Ensure correct serving of html, css, js, json, csv
    if os.path.exists(os.path.join(BASE_DIR, path)):
        return send_from_directory(".", path)
    return send_from_directory(".", "index.html")

# ==============================================================================
# REST API ENDPOINTS
# ==============================================================================

@app.route("/api/autocomplete", methods=["GET"])
def api_autocomplete():
    """
    AVL Tree Prefix Search for Smart Autocomplete.
    Calculates actual time in ms.
    Example: /api/autocomplete?q=lap
    """
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({
            "prefix": "",
            "suggestions": [],
            "search_time_ms": 0.0,
            "search_method": "AVL Tree",
            "complexity": "O(log N)"
        })

    result = store.avl_tree.prefix_search(query, limit=10)
    return jsonify(result)

@app.route("/api/search", methods=["GET"])
def api_search():
    """
    Search products using AVL Tree key lookup and multi-token matching.
    Calculates exact search time.
    """
    start_time = time.perf_counter()
    query = request.args.get("q", "").strip().lower()
    
    if not query:
        # Return popular first 24 products
        sample = [p.to_dict() for p in store.products[:24]]
        return jsonify({
            "query": "",
            "products": sample,
            "total": len(store.products),
            "search_time_ms": 0.0,
            "search_method": "Catalog Scan",
            "complexity": "O(1)"
        })

    # Step 1: Query AVL Tree prefix/exact
    avl_res = store.avl_tree.prefix_search(query, limit=50)
    matched_ids = set(avl_res.get("product_ids", []))

    # Step 2: Fallback query tokenization for multi-word queries
    tokens = [t for t in query.split() if len(t) > 1]
    if len(tokens) > 1 or len(matched_ids) < 10:
        for p in store.products:
            name_lower = p.name.lower()
            cat_lower = p.category.lower()
            brand_lower = p.brand.lower()
            kw_lower = p.keywords.lower()
            
            if all(t in name_lower or t in cat_lower or t in brand_lower or t in kw_lower for t in tokens):
                matched_ids.add(p.id)
            if len(matched_ids) >= 120:
                break

    matched_products = [store.product_map[pid].to_dict() for pid in matched_ids if pid in store.product_map]
    # Sort matched products by rating descending
    matched_products.sort(key=lambda x: (x["Rating"], -x["Price"]), reverse=True)

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0

    return jsonify({
        "query": query,
        "products": matched_products[:60],
        "total": len(matched_products),
        "search_time_ms": round(elapsed_ms, 4),
        "search_method": "AVL Tree",
        "tree_height": store.avl_tree.get_height(store.avl_tree.root),
        "total_nodes": store.avl_tree.total_nodes,
        "complexity": "O(log N)"
    })

@app.route("/api/products", methods=["GET"])
def api_products():
    """
    Get paginated products with optional category, brand, sorting.
    """
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 24))
    sort_by = request.args.get("sort", "rating_desc") # price_asc, price_desc, rating_desc, name_asc
    
    prods = [p.to_dict() for p in store.products]
    
    if sort_by == "price_asc":
        prods.sort(key=lambda x: x["Price"])
    elif sort_by == "price_desc":
        prods.sort(key=lambda x: x["Price"], reverse=True)
    elif sort_by == "name_asc":
        prods.sort(key=lambda x: x["Name"])
    else:
        prods.sort(key=lambda x: x["Rating"], reverse=True)

    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated = prods[start_idx:end_idx]

    return jsonify({
        "products": paginated,
        "total": len(prods),
        "page": page,
        "limit": limit,
        "total_pages": (len(prods) + limit - 1) // limit
    })

@app.route("/api/product/<product_id>", methods=["GET"])
def api_product_detail(product_id):
    """Returns single product details."""
    prod = store.product_map.get(product_id)
    if not prod:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(prod.to_dict())

@app.route("/api/filter", methods=["POST"])
def api_filter():
    """
    DMGT Set Operations Filter Endpoint.
    Receives JSON with categories, brands, minPrice, maxPrice, minRating, inStock.
    Returns filtered products and mathematical formula representation.
    """
    data = request.get_json() or {}
    categories = data.get("categories", [])
    brands = data.get("brands", [])
    min_price = data.get("minPrice")
    max_price = data.get("maxPrice")
    min_rating = data.get("minRating")
    in_stock_only = data.get("inStockOnly", False)
    sort_by = data.get("sortBy", "rating_desc")
    page = int(data.get("page", 1))
    limit = int(data.get("limit", 24))

    filter_res = store.filter_engine.filter_products(
        categories=categories,
        brands=brands,
        min_price=min_price,
        max_price=max_price,
        min_rating=min_rating,
        in_stock_only=in_stock_only
    )

    matching_ids = filter_res["matching_ids"]
    matched_prods = [store.product_map[pid].to_dict() for pid in matching_ids if pid in store.product_map]

    # Sort
    if sort_by == "price_asc":
        matched_prods.sort(key=lambda x: x["Price"])
    elif sort_by == "price_desc":
        matched_prods.sort(key=lambda x: x["Price"], reverse=True)
    elif sort_by == "name_asc":
        matched_prods.sort(key=lambda x: x["Name"])
    else:
        matched_prods.sort(key=lambda x: x["Rating"], reverse=True)

    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated = matched_prods[start_idx:end_idx]

    return jsonify({
        "products": paginated,
        "total": len(matched_prods),
        "page": page,
        "limit": limit,
        "total_pages": (len(matched_prods) + limit - 1) // limit if matched_prods else 0,
        "math_formula": filter_res["math_formula"],
        "filter_time_ms": filter_res["filter_time_ms"],
        "operation": filter_res["operation"],
        "universe_size": filter_res["universe_size"]
    })

@app.route("/api/recommend/<product_id>", methods=["GET"])
def api_recommend(product_id):
    """
    Cosine Similarity Recommendation Endpoint.
    Calculates top 5 similar products dynamically based on descriptions.
    """
    top_n = int(request.args.get("top", 5))
    recs = store.recommender.get_recommendations(product_id, top_n=top_n)
    return jsonify({
        "productId": product_id,
        "method": "Python Cosine Similarity (TF-IDF Vector Space Model)",
        "recommendations": recs
    })

@app.route("/api/order", methods=["POST"])
def api_create_order():
    """Places a simulated demo order."""
    data = request.get_json() or {}
    if not data.get("items"):
        return jsonify({"error": "Cart is empty"}), 400

    order_dict = store.add_order(data)
    return jsonify({
        "message": "Order Placed Successfully",
        "order": order_dict
    }), 201

@app.route("/api/orders", methods=["GET"])
def api_get_orders():
    """Returns past demo orders for My Orders page."""
    return jsonify({
        "orders": store.orders,
        "total": len(store.orders)
    })

@app.route("/api/meta", methods=["GET"])
def api_metadata():
    """Returns available categories, brands, price extremes for filter UI."""
    categories = sorted(list(store.filter_engine.category_sets.keys()))
    brands = sorted(list(store.filter_engine.brand_sets.keys()))
    prices = [p.price for p in store.products]
    min_p = min(prices) if prices else 0
    max_p = max(prices) if prices else 300000

    return jsonify({
        "categories": categories,
        "brands": brands,
        "minPrice": min_p,
        "maxPrice": max_p,
        "totalProducts": len(store.products),
        "avlTree": store.avl_tree.get_stats()
    })

if __name__ == "__main__":
    print("\n=======================================================")
    print(" Smart Search Online Store Server Starting...")
    print(" Direct URL: http://127.0.0.1:5000")
    print("=======================================================\n")
    app.run(host="127.0.0.1", port=5000, debug=False)
