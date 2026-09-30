# Smart Search Autocomplete for an Online Store
**A Complete College Mini-Project Integrating ADSA, DMGT, OOP, and Python NLP**

---

## 🌟 Project Overview
**Smart Search Autocomplete for an Online Store** is an electronics e-commerce platform that implements:
- **ADSA (Advanced Data Structures & Algorithms):** Authentic Self-Balancing **AVL Tree** for $O(\log N)$ product search and prefix autocomplete.
- **DMGT (Discrete Mathematics & Graph Theory):** Mathematical **Set Theory operations** ($\cap$ intersection, $\cup$ union) for multi-attribute product filtering.
- **OOP (Object-Oriented Programming):** Clean domain model classes (`Product`, `Cart`, `CartItem`, `Customer`, `Order`, `OrderItem`, `SearchEngine`, `Recommender`).
- **Python NLP Machine Learning:** Dynamic **TF-IDF Vector Space Model & Cosine Similarity** for computing product recommendations from descriptions and specifications.

---

## 📁 Single-Folder Architecture
All project files are directly inside the **`Smart-Search-Online-Store/`** folder without unnecessary nested directories:

```
Smart-Search-Online-Store/
│
├── index.html          # Homepage with live AVL Autocomplete search & hero stats
├── products.html       # Products catalog with live DMGT Set Operations filtering
├── product.html        # Product details page with dynamic Cosine Similarity recommendations
├── cart.html           # Interactive Shopping Cart management & price calculations
├── checkout.html       # Customer address form & simulated payment gateway
├── orders.html         # "My Orders" order history and tracking
├── style.css           # Modern, responsive CSS design system (mobile/tablet/desktop)
├── script.js           # OOP JavaScript (Product, Cart, Search, DMGT Filter Client)
├── products.csv        # 5,050 realistic sample electronics products across 15 categories
├── app.py              # Flask server coordinating AVL Tree, DMGT Filter, & APIs
├── recommender.py      # TF-IDF Vectorizer & Cosine Similarity recommender engine
├── avl_tree.py         # Python AVL Tree with rotations (LL, RR, LR, RL) & search timer
├── avl_tree.java       # Standalone Java AVL Tree implementation for academic review
├── generate_data.py    # Automatic dataset generator for 5,000+ realistic products
├── run.bat             # 1-Click launcher script for Windows
├── README.md           # Complete project documentation & viva guide
└── requirements.txt    # Project Python dependencies
```

---

## 🚀 Quick Start Guide (One Simple Command)

### 1. Requirements
- Python 3.8 or higher installed on your computer.
- Modern web browser (Chrome, Edge, Firefox, Safari).

### 2. Installation
Open a terminal inside the project directory:
```bash
cd "Smart-Search-Online-Store"
pip install -r requirements.txt
```

*(Dependencies: `flask`, `flask-cors`, `numpy`, `pandas`, `scikit-learn`)*

### 3. Launch Application
Run the one-command start:
```bash
python app.py
```
*(Or on Windows, simply double-click `run.bat`)*

Then open your browser at:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🧪 Step-by-Step Academic Demo Walkthrough

Run the live demo following this sequence:

1. **Homepage & Smart Autocomplete:**
   - Go to `http://127.0.0.1:5000`.
   - In the search bar, type `lap`.
   - **Observe:** Dropdown immediately opens showing autocomplete suggestions:
     - *Laptop*
     - *Laptop Stand*
     - *Laptop Charger*
     - *Gaming Laptop*
     - *Laptop Bag*
   - Note the search metadata badge: `Search Method: AVL Tree` and the real search time (e.g., `⚡ 0.12 ms`).

2. **AVL Tree Search Results:**
   - Press **Enter** or click on any suggestion (e.g. *Laptop*).
   - You are redirected to `products.html?q=laptop`.
   - The banner displays: `Search Method: AVL Tree (O(log N))` with actual height ($H=16$) and search time.

3. **DMGT Set Operations Filtering:**
   - In `products.html`, select:
     - Categories: **Laptops**
     - Brand: **Apple** or **Dell**
     - Price Range: **₹40,000** to **₹150,000**
     - Rating: **★ 4.0 & above**
     - Check: **In Stock Only**
   - Click **Apply DMGT Filter**.
   - **Observe the Active Formula Banner:**
     $$\text{S\_result} = (\text{Laptops}) \cap (\text{Apple} \cup \text{Dell}) \cap (\text{Price} \le 150000) \cap (\text{Rating} \ge 4.0\star) \cap (\text{Stock} > 0)$$
   - Notice the exact set cardinality $|S_{result}|$ and execution time displayed.

4. **Product Details & Dynamic Recommendations:**
   - Click on any product card (e.g., *Dell ProBook 450*).
   - View the detailed specifications, pricing, MRP discount, stock count, and images.
   - Scroll down to **"You May Also Like"**:
     - The top 5 recommendations are **dynamically computed** via Python Cosine Similarity on product descriptions!
     - Displays similarity percentage badge (e.g. `96% Match`).

5. **Shopping Cart Management:**
   - Click **Add to Shopping Cart** (or adjust quantity to 2).
   - Go to `cart.html`.
   - Test increasing (`+`) and decreasing (`-`) item quantity.
   - Check automated calculations:
     - Item Subtotal
     - 18% GST Tax
     - Free Express Shipping
     - Grand Total

6. **Checkout & Payment Simulation:**
   - Click **Proceed to Checkout**.
   - Fill in customer details (Name, Phone, Email, Delivery Address, City, State, PIN).
   - Select **Demo Cash on Delivery** or **Demo Online Payment**.
   - If *Demo Online Payment* is selected, an interactive payment modal appears simulating a UPI QR scan / card gateway.
   - Click **Place Order**.

7. **Order Confirmation & Unique Order ID:**
   - Order confirmation displays:
     - Unique Order ID: **`ORD-1002`**
     - Customer name and delivery destination
     - Products, quantities, and totals
     - Payment status: **Confirmed**

8. **"My Orders" History:**
   - Click **My Orders** in the navigation bar.
   - View previously placed orders with full breakdown and receipt summary.

---

## 🔬 Subject Integration Details

### 1. ADSA: Authentic Self-Balancing AVL Tree
An AVL (Adelson-Velsky and Landis) Tree is a self-balancing binary search tree where the heights of the two child subtrees of any node differ by at most one:
$$| \text{height}(\text{left}) - \text{height}(\text{right}) | \le 1$$

- **Rotations Implemented:**
  - **Left-Left (LL):** Single Right Rotation
  - **Right-Right (RR):** Single Left Rotation
  - **Left-Right (LR):** Left Rotation on left child, followed by Right Rotation on node
  - **Right-Left (RL):** Right Rotation on right child, followed by Left Rotation on node
- **Search Time Complexity:** $O(\log N)$
- **Prefix Autocomplete Time Complexity:** $O(\log N + K)$ where $K$ is the number of matching suggestions.
- **Tree Verification:** Standalone Java code is also available in `avl_tree.java`.

### 2. DMGT: Discrete Mathematics Set Theory Filter
Product filtering is modeled using set algebra:
- **Universe ($U$):** All 5,050 products.
- **Category Union Set:** $S_{cat} = \bigcup_{c \in C} S(c)$
- **Brand Union Set:** $S_{brand} = \bigcup_{b \in B} S(b)$
- **Price Interval Set:** $S_{price} = \{p \in U \mid \text{min\_p} \le p.price \le \text{max\_p}\}$
- **Rating Set:** $S_{rating} = \{p \in U \mid p.rating \ge \text{min\_r}\}$
- **Stock Set:** $S_{stock} = \{p \in U \mid p.stock > 0\}$
- **Filtered Result Set:**
  $$S_{result} = S_{cat} \cap S_{brand} \cap S_{price} \cap S_{rating} \cap S_{stock}$$

### 3. OOP: Object-Oriented Programming Concepts
- **Encapsulation:** Properties and methods are wrapped inside classes.
- **Classes Defined:**
  - `Product`: encapsulating product attributes, stock validation, and price formatting.
  - `CartItem`: managing item quantity, stock limits, and subtotal.
  - `Cart`: managing items map, add/remove, subtotal, tax, and storage synchronization.
  - `Customer`: encapsulating contact info and form validation.
  - `OrderItem`: individual line item with subtotal calculation.
  - `Order`: unique order ID sequence, customer mapping, status transitions, and audit records.
  - `SearchEngineClient`: debounce mechanism, prefix lookup, and dropdown renderer.
  - `DMGTFilterEngine`: set intersection and union algebra.

### 4. Python: Dynamic Cosine Similarity Recommender
- Uses Term Frequency - Inverse Document Frequency (**TF-IDF**):
  $$\text{TF}(t, d) = \text{count}(t \in d)$$
  $$\text{IDF}(t) = \ln\left(\frac{1 + N}{1 + \text{DF}(t)}\right) + 1$$
- Converts product descriptions and technical specifications into $L_2$-normalized vectors $\vec{u}$ and $\vec{v}$.
- Computes **Cosine Similarity**:
  $$\text{Cosine Similarity}(\vec{u}, \vec{v}) = \frac{\vec{u} \cdot \vec{v}}{\|\vec{u}\| \|\vec{v}\|}$$
- Returns the top 5 most similar products dynamically at runtime without hardcoding.

---

## ❓ Academic Viva Questions & Answers

1. **Why use an AVL Tree instead of a standard BST?**  
   *Answer:* Standard Binary Search Trees can degrade to $O(N)$ worst-case time complexity if keys are inserted in sorted or semi-sorted order (skewed tree). The AVL Tree enforces strict balancing with $|h_L - h_R| \le 1$ using 4 rotation types (LL, RR, LR, RL), guaranteeing strict $O(\log N)$ search time.

2. **How does the autocomplete search work on the AVL Tree?**  
   *Answer:* The prefix search locates the subtree containing keys starting with the search prefix using BST ordering, and then traverses matching nodes to collect autocomplete suggestions in $O(\log N + K)$ time.

3. **How does DMGT Set Theory apply to e-commerce filtering?**  
   *Answer:* Products with multiple attributes (Category, Brand, Price, Rating) can each be represented as mathematical subsets of the universal product set $U$. Multiple selections within a category represent set union ($\cup$), while multi-attribute criteria represent set intersection ($\cap$).

4. **Why is Cosine Similarity suitable for product recommendations?**  
   *Answer:* Cosine Similarity measures the cosine of the angle between two multi-dimensional feature vectors regardless of description length. It matches semantic features (chips, RAM, battery life, display technology) between products accurately.

---

## 👨‍💻 Author & Submission
- **Project Title:** Smart Search Autocomplete for an Online Store
- **Subjects:** ADSA, DMGT, OOP, Python
- **Dataset Size:** 5,050 Realistic Electronics Products
- **Execution:** One-Command Local Server (`python app.py`)
