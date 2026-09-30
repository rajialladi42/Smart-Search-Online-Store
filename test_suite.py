"""
test_suite.py
Integration test suite for Smart Search Online Store.
Tests all endpoints, AVL tree search, DMGT filtering, and dynamic recommendations.
"""

import json
import urllib.request

BASE_URL = "http://127.0.0.1:5000"

def request_json(path, method="GET", payload=None):
    url = f"{BASE_URL}{path}"
    data = json.dumps(payload).encode("utf-8") if payload else None
    headers = {"Content-Type": "application/json"} if payload else {}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))

def test_pages():
    print("\n[TEST 1] Static HTML Pages & Assets...")
    pages = [
        "/",
        "/products.html",
        "/product.html",
        "/cart.html",
        "/checkout.html",
        "/orders.html",
        "/style.css",
        "/script.js"
    ]
    for p in pages:
        req = urllib.request.Request(f"{BASE_URL}{p}")
        with urllib.request.urlopen(req) as resp:
            content = resp.read()
            assert resp.status == 200, f"Failed to load {p}"
            print(f"  [OK] {p:<16} : HTTP 200 OK ({len(content):,} bytes)")

def test_avl_autocomplete():
    print("\n[TEST 2] ADSA - AVL Tree Prefix Autocomplete (query='lap')...")
    status, data = request_json("/api/autocomplete?q=lap")
    assert status == 200
    assert data["search_method"] == "AVL Tree"
    print(f"  [OK] Search Method    : {data['search_method']}")
    print(f"  [OK] Complexity       : {data['complexity']}")
    print(f"  [OK] Measured Time    : {data['search_time_ms']} ms")
    print(f"  [OK] AVL Tree Height  : {data['tree_height']}")
    print(f"  [OK] Indexed Nodes    : {data['total_nodes']}")
    print(f"  [OK] Suggestions Returned: {len(data['suggestions'])}")
    for s in data["suggestions"][:5]:
        print(f"      -> {s['suggestion']} ({s['product_count']} products)")

def test_avl_search():
    print("\n[TEST 3] ADSA - AVL Tree Product Search (query='laptop')...")
    status, data = request_json("/api/search?q=laptop")
    assert status == 200
    print(f"  [OK] Search Time      : {data['search_time_ms']} ms")
    print(f"  [OK] Matched Products : {data['total']}")
    assert data["total"] > 0

def test_dmgt_filter():
    print("\n[TEST 4] DMGT - Set Operations Product Filter...")
    payload = {
        "categories": ["Laptops"],
        "brands": ["Apple", "Dell"],
        "minPrice": 50000,
        "maxPrice": 200000,
        "minRating": 4.0,
        "inStockOnly": True
    }
    status, data = request_json("/api/filter", method="POST", payload=payload)
    assert status == 200
    print(f"  [OK] Operation        : {data['operation'].encode('ascii', 'replace').decode('ascii')}")
    print(f"  [OK] Math Formula     : {data['math_formula'].encode('ascii', 'replace').decode('ascii')}")
    print(f"  [OK] Set Cardinality  : |S_result| = {data['total']} items")
    print(f"  [OK] Filter Time      : {data['filter_time_ms']} ms")

def test_python_recommendations():
    print("\n[TEST 5] Python - Cosine Similarity Recommendations...")
    status, data = request_json("/api/recommend/PROD-1001")
    assert status == 200
    recs = data["recommendations"]
    print(f"  [OK] Method           : {data['method']}")
    print(f"  [OK] Dynamic Recs     : {len(recs)} returned")
    for r in recs:
        print(f"      -> {r['Name']}")
        print(f"         Match Score : {r['similarity_percentage']} ({r['similarity_score']})")
        print(f"         Reason      : {r['recommendation_reason']}")

def test_order_creation():
    print("\n[TEST 6] Order Creation & Checkout Flow...")
    payload = {
        "customer": {
            "name": "Jane Developer",
            "phone": "9876543210",
            "email": "jane.dev@college.edu",
            "address": "404 Innovation Hub",
            "city": "Bengaluru",
            "state": "Karnataka",
            "pincode": "560001"
        },
        "items": [
            {
                "productId": "PROD-1001",
                "productName": "Dell ProBook 450 Creator Series",
                "price": 173700,
                "quantity": 1,
                "subtotal": 173700
            }
        ],
        "totalAmount": 173700,
        "paymentMethod": "Demo Online Payment (Simulated UPI)"
    }
    status, data = request_json("/api/order", method="POST", payload=payload)
    assert status == 201
    ord_info = data["order"]
    print(f"  [OK] Confirmation Msg : {data['message']}")
    print(f"  [OK] Unique Order ID  : {ord_info['orderId']}")
    print(f"  [OK] Payment Method   : {ord_info['paymentMethod']}")
    print(f"  [OK] Total Amount     : Rs. {ord_info['totalAmount']:,}")

def test_orders_history():
    print("\n[TEST 7] My Orders Page API...")
    status, data = request_json("/api/orders")
    assert status == 200
    print(f"  [OK] Total Saved Orders: {data['total']}")
    for o in data["orders"][:3]:
        print(f"      -> {o['orderId']} | Total: Rs. {o['totalAmount']:,} | Status: {o['status']}")

if __name__ == "__main__":
    print("==================================================")
    print(" Smart Search Online Store - Automated Test Suite")
    print("==================================================")
    test_pages()
    test_avl_autocomplete()
    test_avl_search()
    test_dmgt_filter()
    test_python_recommendations()
    test_order_creation()
    test_orders_history()
    print("\n>>> ALL TESTS PASSED SUCCESSFULLY (100% OPERATIONAL)!")
    print("==================================================")
