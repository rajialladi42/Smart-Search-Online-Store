/**
 * script.js - Smart Search Online Store
 * Object-Oriented Frontend Architecture
 * 
 * Demonstrates OOP:
 * - Product, CartItem, Cart, Customer, OrderItem, Order
 * Integrates:
 * - ADSA: Real-time AVL Tree Autocomplete & Search
 * - DMGT: Discrete Mathematics Set Operations Filter Formula
 * - Python: Cosine Similarity Recommendations
 */

// ==============================================================================
// OOP DOMAIN CLASSES
// ==============================================================================

class Product {
  constructor(data) {
    this.id = data.ID || data.id;
    this.name = data.Name || data.name;
    this.category = data.Category || data.category;
    this.brand = data.Brand || data.brand;
    this.price = parseFloat(data.Price || data.price || 0);
    this.rating = parseFloat(data.Rating || data.rating || 0);
    this.stock = parseInt(data.Stock || data.stock || 0);
    this.description = data.Description || data.description || "";
    this.image = data.Image || data.image || "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=600";
    this.keywords = data.Keywords || data.keywords || "";
  }

  isInStock() {
    return this.stock > 0;
  }

  getFormattedPrice() {
    return '₹' + this.price.toLocaleString('en-IN');
  }

  getMRP() {
    return '₹' + Math.round(this.price * 1.25).toLocaleString('en-IN');
  }
}

class CartItem {
  constructor(product, quantity = 1) {
    this.product = product instanceof Product ? product : new Product(product);
    this.quantity = parseInt(quantity) || 1;
  }

  getSubtotal() {
    return this.product.price * this.quantity;
  }

  increment() {
    if (this.quantity < this.product.stock) {
      this.quantity++;
      return true;
    }
    return false;
  }

  decrement() {
    if (this.quantity > 1) {
      this.quantity--;
      return true;
    }
    return false;
  }

  toJSON() {
    return {
      product: this.product,
      quantity: this.quantity
    };
  }
}

class Cart {
  constructor() {
    this.items = new Map(); // key: productId -> CartItem
    this.loadFromStorage();
  }

  addItem(product, quantity = 1) {
    const prodObj = product instanceof Product ? product : new Product(product);
    if (!prodObj.isInStock()) {
      return { success: false, message: "Sorry, this product is currently out of stock!" };
    }

    if (this.items.has(prodObj.id)) {
      const item = this.items.get(prodObj.id);
      item.quantity += quantity;
    } else {
      this.items.set(prodObj.id, new CartItem(prodObj, quantity));
    }

    this.saveToStorage();
    return { success: true, message: `Added ${prodObj.name} to cart!` };
  }

  removeItem(productId) {
    if (this.items.has(productId)) {
      this.items.delete(productId);
      this.saveToStorage();
      return true;
    }
    return false;
  }

  updateQuantity(productId, quantity) {
    if (this.items.has(productId)) {
      const q = parseInt(quantity);
      if (q <= 0) {
        this.removeItem(productId);
      } else {
        this.items.get(productId).quantity = q;
        this.saveToStorage();
      }
      return true;
    }
    return false;
  }

  clear() {
    this.items.clear();
    this.saveToStorage();
  }

  getItemList() {
    return Array.from(this.items.values());
  }

  getTotalQuantity() {
    let total = 0;
    for (const item of this.items.values()) {
      total += item.quantity;
    }
    return total;
  }

  getSubtotal() {
    let sum = 0;
    for (const item of this.items.values()) {
      sum += item.getSubtotal();
    }
    return sum;
  }

  getTax() {
    // 18% GST standard electronics
    return Math.round(this.getSubtotal() * 0.18);
  }

  getShipping() {
    return this.getSubtotal() > 999 || this.getSubtotal() === 0 ? 0 : 99;
  }

  getGrandTotal() {
    return this.getSubtotal() + this.getTax() + this.getShipping();
  }

  saveToStorage() {
    try {
      const serialized = Array.from(this.items.entries()).map(([k, item]) => [k, item.toJSON()]);
      localStorage.setItem("smart_store_cart", JSON.stringify(serialized));
      AppUI.updateCartBadge();
    } catch (e) {
      console.error("Error saving cart to localStorage:", e);
    }
  }

  loadFromStorage() {
    try {
      const raw = localStorage.getItem("smart_store_cart");
      if (raw) {
        const parsed = JSON.parse(raw);
        this.items = new Map();
        for (const [k, itemObj] of parsed) {
          const prod = new Product(itemObj.product);
          this.items.set(k, new CartItem(prod, itemObj.quantity));
        }
      }
    } catch (e) {
      console.error("Error loading cart:", e);
      this.items = new Map();
    }
  }
}

class Customer {
  constructor(name, phone, email, address, city, state, pincode) {
    this.name = (name || "").trim();
    this.phone = (phone || "").trim();
    this.email = (email || "").trim();
    this.address = (address || "").trim();
    this.city = (city || "").trim();
    this.state = (state || "").trim();
    this.pincode = (pincode || "").trim();
  }

  validate() {
    if (!this.name) return { valid: false, message: "Please enter your full name." };
    if (!this.phone || this.phone.length < 10) return { valid: false, message: "Please enter a valid 10-digit mobile number." };
    if (!this.email || !this.email.includes("@")) return { valid: false, message: "Please enter a valid email address." };
    if (!this.address) return { valid: false, message: "Please enter your delivery street address." };
    if (!this.city) return { valid: false, message: "Please enter your city." };
    if (!this.state) return { valid: false, message: "Please enter your state." };
    if (!this.pincode || this.pincode.length < 6) return { valid: false, message: "Please enter a valid 6-digit PIN code." };
    return { valid: true };
  }

  toJSON() {
    return {
      name: this.name,
      phone: this.phone,
      email: this.email,
      address: this.address,
      city: this.city,
      state: this.state,
      pincode: this.pincode
    };
  }
}

class OrderItem {
  constructor(productId, productName, price, quantity) {
    this.productId = productId;
    this.productName = productName;
    this.price = parseFloat(price);
    this.quantity = parseInt(quantity);
    this.subtotal = this.price * this.quantity;
  }
}

class Order {
  constructor(customer, items, totalAmount, paymentMethod, orderId = null, orderDate = null) {
    this.orderId = orderId || `ORD-${Math.floor(1000 + Math.random() * 9000)}`;
    this.customer = customer;
    this.items = items;
    this.totalAmount = totalAmount;
    this.paymentMethod = paymentMethod;
    this.status = "Confirmed";
    this.orderDate = orderDate || new Date().toLocaleString();
  }

  toJSON() {
    return {
      orderId: this.orderId,
      customer: this.customer instanceof Customer ? this.customer.toJSON() : this.customer,
      items: this.items.map(i => ({
        productId: i.productId,
        productName: i.productName,
        price: i.price,
        quantity: i.quantity,
        subtotal: i.subtotal
      })),
      totalAmount: this.totalAmount,
      paymentMethod: this.paymentMethod,
      status: this.status,
      orderDate: this.orderDate
    };
  }
}

// Global Singletons
const globalCart = new Cart();

// ==============================================================================
// SEARCH CLIENT (ADSA AVL TREE AUTOCOMPLETE)
// ==============================================================================

class SearchEngineClient {
  static debounceTimer = null;

  static initAutocomplete(inputId, dropdownId, heroSearch = false) {
    const input = document.getElementById(inputId);
    const dropdown = document.getElementById(dropdownId);
    if (!input || !dropdown) return;

    input.addEventListener("input", (e) => {
      const q = e.target.value.trim();
      clearTimeout(SearchEngineClient.debounceTimer);

      if (q.length < 2) {
        dropdown.classList.remove("active");
        dropdown.innerHTML = "";
        return;
      }

      SearchEngineClient.debounceTimer = setTimeout(() => {
        SearchEngineClient.fetchAutocomplete(q, dropdown, input);
      }, 150); // Fast responsive debounce
    });

    // Close on click outside
    document.addEventListener("click", (e) => {
      if (!input.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.classList.remove("active");
      }
    });

    // Enter key submits search
    input.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        const term = input.value.trim();
        if (term) {
          window.location.href = `products.html?q=${encodeURIComponent(term)}`;
        }
      }
    });
  }

  static async fetchAutocomplete(query, dropdown, input) {
    try {
      const resp = await fetch(`/api/autocomplete?q=${encodeURIComponent(query)}`);
      if (!resp.ok) return;
      const data = await resp.json();

      const suggestions = data.suggestions || [];
      const searchTime = data.search_time_ms || 0.0;
      const treeHeight = data.tree_height || 16;
      const totalNodes = data.total_nodes || 7643;

      if (suggestions.length === 0) {
        dropdown.innerHTML = `
          <div class="autocomplete-header">
            <span>Search Method: <strong>AVL Tree (O(log N))</strong></span>
            <span class="avl-meta-pill">⚡ ${searchTime.toFixed(3)} ms</span>
          </div>
          <div style="padding: 1rem; color: var(--text-muted); font-size: 0.85rem; text-align: center;">
            No direct prefix match in AVL Tree. Press Enter to search catalog.
          </div>
        `;
        dropdown.classList.add("active");
        return;
      }

      let html = `
        <div class="autocomplete-header">
          <span>Search Method: <strong>AVL Tree (Height: ${treeHeight})</strong></span>
          <span class="avl-meta-pill">⚡ ${searchTime.toFixed(3)} ms</span>
        </div>
      `;

      suggestions.forEach((item) => {
        const text = item.suggestion;
        const count = item.product_count;
        const qRegex = new RegExp(`(${query})`, "gi");
        const highlighted = text.replace(qRegex, '<span class="autocomplete-highlight">$1</span>');

        html += `
          <div class="autocomplete-item" data-term="${text}">
            <div class="autocomplete-text">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
              <span>${highlighted}</span>
            </div>
            ${count > 0 ? `<span class="autocomplete-count">${count} items</span>` : '<span class="autocomplete-count">Suggestion</span>'}
          </div>
        `;
      });

      dropdown.innerHTML = html;
      dropdown.classList.add("active");

      // Bind click on items
      dropdown.querySelectorAll(".autocomplete-item").forEach((el) => {
        el.addEventListener("click", () => {
          const term = el.getAttribute("data-term");
          input.value = term;
          dropdown.classList.remove("active");
          window.location.href = `products.html?q=${encodeURIComponent(term)}`;
        });
      });

    } catch (err) {
      console.error("Autocomplete fetch error:", err);
    }
  }
}

// ==============================================================================
// DMGT FILTER CLIENT
// ==============================================================================

class DMGTFilterClient {
  constructor(onFilterChanged) {
    this.onFilterChanged = onFilterChanged;
    this.categories = new Set();
    this.brands = new Set();
    this.minPrice = null;
    this.maxPrice = null;
    this.minRating = null;
    this.inStockOnly = false;
    this.sortBy = "rating_desc";
    this.currentPage = 1;
  }

  getFormulaExpression() {
    const parts = [];
    if (this.categories.size > 0) {
      parts.push(`(Cat: ${Array.from(this.categories).join(" ∪ ")})`);
    }
    if (this.brands.size > 0) {
      parts.push(`(Brand: ${Array.from(this.brands).join(" ∪ ")})`);
    }
    if (this.minPrice !== null || this.maxPrice !== null) {
      const minStr = this.minPrice ? `₹${this.minPrice}` : '₹0';
      const maxStr = this.maxPrice ? `₹${this.maxPrice}` : 'Max';
      parts.push(`(Price: ${minStr} - ${maxStr})`);
    }
    if (this.minRating) {
      parts.push(`(Rating ≥ ${this.minRating}★)`);
    }
    if (this.inStockOnly) {
      parts.push(`(Stock > 0)`);
    }
    return parts.length > 0 ? `S_result = ${parts.join(" ∩ ")}` : "S_result = Universe (U)";
  }

  async executeFilter() {
    const payload = {
      categories: Array.from(this.categories),
      brands: Array.from(this.brands),
      minPrice: this.minPrice,
      maxPrice: this.maxPrice,
      minRating: this.minRating,
      inStockOnly: this.inStockOnly,
      sortBy: this.sortBy,
      page: this.currentPage,
      limit: 24
    };

    try {
      const resp = await fetch("/api/filter", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await resp.json();
      if (this.onFilterChanged) {
        this.onFilterChanged(data, this.getFormulaExpression());
      }
    } catch (e) {
      console.error("Filter error:", e);
    }
  }

  reset() {
    this.categories.clear();
    this.brands.clear();
    this.minPrice = null;
    this.maxPrice = null;
    this.minRating = null;
    this.inStockOnly = false;
    this.currentPage = 1;
    this.executeFilter();
  }
}

// ==============================================================================
// UI HELPERS & NOTIFICATIONS
// ==============================================================================

class AppUI {
  static showToast(message, type = "success") {
    let container = document.getElementById("toast-container");
    if (!container) {
      container = document.createElement("div");
      container.id = "toast-container";
      container.className = "toast-container";
      document.body.appendChild(container);
    }

    const toast = document.createElement("div");
    toast.className = "toast";
    const icon = type === "success" ? "✓" : "ℹ";
    toast.innerHTML = `<span style="color: ${type === 'success' ? '#10b981' : '#6366f1'}; font-weight:800;">${icon}</span> <span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = "0";
      toast.style.transform = "translateX(100%)";
      toast.style.transition = "all 0.3s ease";
      setTimeout(() => toast.remove(), 300);
    }, 3200);
  }

  static updateCartBadge() {
    const count = globalCart.getTotalQuantity();
    document.querySelectorAll(".cart-badge").forEach((el) => {
      el.textContent = count;
      el.style.display = count > 0 ? "inline-block" : "none";
    });
  }

  static renderProductCard(p, isRecommendation = false) {
    const prod = p instanceof Product ? p : new Product(p);
    const inStock = prod.isInStock();
    const simBadge = p.similarity_percentage ? `
      <div class="match-similarity-pill">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"></polyline></svg>
        <span>${p.similarity_percentage} Match</span>
      </div>
    ` : '';

    return `
      <div class="product-card" data-id="${prod.id}">
        <div class="product-image-wrap">
          <a href="product.html?id=${prod.id}">
            <img src="${prod.image}" alt="${prod.name}" loading="lazy" onerror="this.src='https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=600'">
          </a>
          ${simBadge}
          <div class="product-badge-rating">
            <span>★</span> ${prod.rating.toFixed(1)}
          </div>
        </div>
        <div class="product-content">
          <div class="product-tags">
            <span class="tag-cat">${prod.category}</span>
            <span class="tag-brand">${prod.brand}</span>
          </div>
          <a href="product.html?id=${prod.id}" class="product-title" title="${prod.name}">
            ${prod.name}
          </a>
          <div class="product-desc-snippet">
            ${p.recommendation_reason || prod.description}
          </div>
          <div class="product-footer">
            <div class="price-wrap">
              <span class="price-label">Price</span>
              <span class="price-value">${prod.getFormattedPrice()}</span>
            </div>
            <button class="btn-add-cart ${inStock ? '' : 'out-of-stock'}" 
                    onclick="handleAddToCart('${prod.id}', event)" 
                    ${inStock ? '' : 'disabled'}>
              ${inStock ? `
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path></svg>
                Add
              ` : 'Sold Out'}
            </button>
          </div>
        </div>
      </div>
    `;
  }
}

// Global Add to Cart click handler
window.handleAddToCart = async function(productId, event) {
  if (event) event.stopPropagation();
  try {
    const resp = await fetch(`/api/product/${productId}`);
    if (resp.ok) {
      const data = await resp.json();
      const res = globalCart.addItem(data, 1);
      if (res.success) {
        AppUI.showToast(res.message, "success");
      } else {
        AppUI.showToast(res.message, "info");
      }
    }
  } catch (e) {
    console.error("Add to cart error:", e);
  }
};

// Mobile Nav Toggle
document.addEventListener("DOMContentLoaded", () => {
  AppUI.updateCartBadge();
  const mobileToggle = document.getElementById("mobile-menu-toggle");
  const navLinks = document.getElementById("nav-links");
  if (mobileToggle && navLinks) {
    mobileToggle.addEventListener("click", () => {
      navLinks.classList.toggle("mobile-open");
    });
  }

  // Initialize navbar search autocomplete if present
  SearchEngineClient.initAutocomplete("nav-search-input", "nav-autocomplete-dropdown");
});
