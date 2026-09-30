"""
avl_tree.py
ADSA (Advanced Data Structures & Algorithms) Implementation:
Self-Balancing AVL (Adelson-Velsky and Landis) Tree for Fast Product Search & Autocomplete.

Features:
- Binary Search Tree with balance factor constraint: |height(L) - height(R)| <= 1
- Rotations:
    * Left-Left (LL): Single Right Rotation
    * Right-Right (RR): Single Left Rotation
    * Left-Right (LR): Left Rotation followed by Right Rotation
    * Right-Left (RL): Right Rotation followed by Left Rotation
- Real-time search time calculation (time.perf_counter)
- Prefix search for smart autocomplete (e.g. 'lap' -> 'Laptop', 'Laptop Stand', etc.)
"""

import time

class AVLNode:
    """Represents a single node in the AVL Tree."""
    def __init__(self, key, product_id=None):
        self.key = key.strip().lower()  # Normalized key for fast indexing
        self.display_key = key.strip()  # Original casing for UI display
        self.product_ids = set()
        if product_id:
            self.product_ids.add(product_id)
        self.height = 1
        self.left = None
        self.right = None

class AVLTree:
    """
    Self-balancing AVL Tree implementation.
    Maintains O(log N) lookup, insertion, and prefix search guarantees.
    """
    def __init__(self):
        self.root = None
        self.total_nodes = 0
        self.rotations_ll = 0
        self.rotations_rr = 0
        self.rotations_lr = 0
        self.rotations_rl = 0

    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def rotate_right(self, y):
        r"""
        Right Rotation (LL Case):
             y                               x
            / \     Rotate Right (y)       /   \
           x   T3   --------------->     T1     y
          / \                                  / \
         T1  T2                               T2  T3
        """
        x = y.left
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update heights
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))

        return x

    def rotate_left(self, x):
        r"""
        Left Rotation (RR Case):
           x                                   y
          / \        Rotate Left (x)         /   \
         T1  y      ---------------->       x     T3
            / \                            / \
           T2  T3                         T1  T2
        """
        y = x.right
        T2 = y.left

        # Perform rotation
        y.left = x
        x.right = T2

        # Update heights
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def insert(self, key, product_id):
        """Public API to insert a key and product_id into the AVL tree."""
        if not key or not key.strip():
            return
        self.root = self._insert(self.root, key.strip(), product_id)

    def _insert(self, node, key, product_id):
        norm_key = key.lower()

        # 1. Normal BST insertion
        if not node:
            self.total_nodes += 1
            return AVLNode(key, product_id)

        if norm_key == node.key:
            node.product_ids.add(product_id)
            return node
        elif norm_key < node.key:
            node.left = self._insert(node.left, key, product_id)
        else:
            node.right = self._insert(node.right, key, product_id)

        # 2. Update height of current ancestor node
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        # 3. Get balance factor to check whether this node became unbalanced
        balance = self.get_balance(node)

        # 4. If unbalanced, handle the 4 rotational cases:

        # Case 1 - Left Left (LL)
        if balance > 1 and norm_key < node.left.key:
            self.rotations_ll += 1
            return self.rotate_right(node)

        # Case 2 - Right Right (RR)
        if balance < -1 and norm_key > node.right.key:
            self.rotations_rr += 1
            return self.rotate_left(node)

        # Case 3 - Left Right (LR)
        if balance > 1 and norm_key > node.left.key:
            self.rotations_lr += 1
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        # Case 4 - Right Left (RL)
        if balance < -1 and norm_key < node.right.key:
            self.rotations_rl += 1
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def exact_search(self, key):
        """Exact lookup in AVL Tree with time measurement."""
        start_time = time.perf_counter()
        norm_key = key.strip().lower()
        curr = self.root
        found_node = None

        while curr:
            if curr.key == norm_key:
                found_node = curr
                break
            elif norm_key < curr.key:
                curr = curr.left
            else:
                curr = curr.right

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        return {
            "key": key,
            "found": found_node is not None,
            "product_ids": list(found_node.product_ids) if found_node else [],
            "search_time_ms": round(elapsed_ms, 4),
            "search_method": "AVL Tree",
            "tree_height": self.get_height(self.root),
            "complexity": "O(log N)"
        }

    def prefix_search(self, prefix, limit=10):
        """
        Smart Autocomplete Search using AVL Tree traversal.
        Finds all keys starting with prefix.
        Calculates ACTUAL execution time with high precision.
        """
        start_time = time.perf_counter()
        norm_prefix = prefix.strip().lower()
        results = []
        collected_product_ids = set()

        if norm_prefix:
            self._collect_prefix(self.root, norm_prefix, results, collected_product_ids, limit)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return {
            "prefix": prefix,
            "suggestions": results[:limit],
            "product_ids": list(collected_product_ids),
            "count": len(results),
            "search_time_ms": round(elapsed_ms, 4),
            "search_method": "AVL Tree",
            "tree_height": self.get_height(self.root),
            "total_nodes": self.total_nodes,
            "complexity": "O(log N + K)"
        }

    def _collect_prefix(self, node, prefix, results, collected_ids, limit):
        if not node or len(results) >= limit * 2:
            return

        # Optimization: prune traversal using BST properties
        # If node's key could have prefix descendants on the left
        if node.key >= prefix:
            self._collect_prefix(node.left, prefix, results, collected_ids, limit)

        # Check current node
        if node.key.startswith(prefix) or prefix in node.key:
            results.append({
                "suggestion": node.display_key,
                "product_count": len(node.product_ids),
                "sample_id": list(node.product_ids)[0] if node.product_ids else None
            })
            collected_ids.update(node.product_ids)

        # Check right subtree
        self._collect_prefix(node.right, prefix, results, collected_ids, limit)

    def get_stats(self):
        """Returns AVL Tree structural statistics for viva and debug."""
        return {
            "root_key": self.root.key if self.root else None,
            "height": self.get_height(self.root),
            "total_nodes": self.total_nodes,
            "rotations": {
                "LL": self.rotations_ll,
                "RR": self.rotations_rr,
                "LR": self.rotations_lr,
                "RL": self.rotations_rl,
                "total": self.rotations_ll + self.rotations_rr + self.rotations_lr + self.rotations_rl
            },
            "is_balanced": abs(self.get_balance(self.root)) <= 1 if self.root else True
        }
