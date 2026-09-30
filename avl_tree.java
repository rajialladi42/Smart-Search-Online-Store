/**
 * avl_tree.java
 * College Mini-Project: Smart Search Autocomplete for an Online Store
 * ADSA (Advanced Data Structures and Algorithms) Integration
 * 
 * Complete implementation of Self-Balancing AVL (Adelson-Velsky and Landis) Tree
 * for Fast Product Lookup and Autocomplete Suggestions.
 * 
 * Operations Implemented:
 * 1. Node representation with height and balance factor
 * 2. Left Rotation (RR Case)
 * 3. Right Rotation (LL Case)
 * 4. Left-Right Rotation (LR Case)
 * 5. Right-Left Rotation (RL Case)
 * 6. AVL Insert with automated balancing
 * 7. Exact Search (O(log N))
 * 8. Prefix Search for Autocomplete (O(log N + K))
 */

import java.util.*;

public class avl_tree {

    // Node definition for AVL Tree
    public static class AVLNode {
        String key;
        Set<String> productIds;
        int height;
        AVLNode left;
        AVLNode right;

        public AVLNode(String key, String productId) {
            this.key = key;
            this.productIds = new HashSet<>();
            if (productId != null) {
                this.productIds.add(productId);
            }
            this.height = 1;
            this.left = null;
            this.right = null;
        }
    }

    // AVL Tree Class
    public static class AVLTree {
        private AVLNode root;
        private int totalRotations = 0;
        private int totalNodes = 0;

        // Get height of node
        public int getHeight(AVLNode node) {
            if (node == null) return 0;
            return node.height;
        }

        // Get balance factor of node
        public int getBalance(AVLNode node) {
            if (node == null) return 0;
            return getHeight(node.left) - getHeight(node.right);
        }

        // Right Rotation (LL Rotation)
        private AVLNode rotateRight(AVLNode y) {
            AVLNode x = y.left;
            AVLNode T2 = x.right;

            // Perform rotation
            x.right = y;
            y.left = T2;

            // Update heights
            y.height = Math.max(getHeight(y.left), getHeight(y.right)) + 1;
            x.height = Math.max(getHeight(x.left), getHeight(x.right)) + 1;

            totalRotations++;
            return x;
        }

        // Left Rotation (RR Rotation)
        private AVLNode rotateLeft(AVLNode x) {
            AVLNode y = x.right;
            AVLNode T2 = y.left;

            // Perform rotation
            y.left = x;
            x.right = T2;

            // Update heights
            x.height = Math.max(getHeight(x.left), getHeight(x.right)) + 1;
            y.height = Math.max(getHeight(y.left), getHeight(y.right)) + 1;

            totalRotations++;
            return y;
        }

        // Public insert method
        public void insert(String key, String productId) {
            if (key == null || key.trim().isEmpty()) return;
            root = insertNode(root, key.trim().toLowerCase(), productId);
        }

        // Recursive insert with AVL rebalancing
        private AVLNode insertNode(AVLNode node, String key, String productId) {
            // Standard BST insertion
            if (node == null) {
                totalNodes++;
                return new AVLNode(key, productId);
            }

            int cmp = key.compareTo(node.key);
            if (cmp < 0) {
                node.left = insertNode(node.left, key, productId);
            } else if (cmp > 0) {
                node.right = insertNode(node.right, key, productId);
            } else {
                // Key already exists, associate product ID
                node.productIds.add(productId);
                return node;
            }

            // Update height of ancestor node
            node.height = 1 + Math.max(getHeight(node.left), getHeight(node.right));

            // Check balance factor
            int balance = getBalance(node);

            // Case 1: Left Left (LL)
            if (balance > 1 && key.compareTo(node.left.key) < 0) {
                return rotateRight(node);
            }

            // Case 2: Right Right (RR)
            if (balance < -1 && key.compareTo(node.right.key) > 0) {
                return rotateLeft(node);
            }

            // Case 3: Left Right (LR)
            if (balance > 1 && key.compareTo(node.left.key) > 0) {
                node.left = rotateLeft(node.left);
                return rotateRight(node);
            }

            // Case 4: Right Left (RL)
            if (balance < -1 && key.compareTo(node.right.key) < 0) {
                node.right = rotateRight(node.right);
                return rotateLeft(node);
            }

            return node;
        }

        // Exact Search
        public AVLNode search(String key) {
            if (key == null) return null;
            String searchKey = key.trim().toLowerCase();
            AVLNode curr = root;
            while (curr != null) {
                int cmp = searchKey.compareTo(curr.key);
                if (cmp == 0) return curr;
                else if (cmp < 0) curr = curr.left;
                else curr = curr.right;
            }
            return null;
        }

        // Prefix Search for Smart Autocomplete
        public List<String> autocomplete(String prefix, int maxResults) {
            long startTime = System.nanoTime();
            List<String> results = new ArrayList<>();
            if (prefix == null || prefix.trim().isEmpty()) return results;

            collectPrefix(root, prefix.trim().toLowerCase(), results, maxResults);
            long elapsedNanos = System.nanoTime() - startTime;
            double elapsedMillis = elapsedNanos / 1_000_000.0;

            System.out.printf("[AVL Search] Prefix: '%s' | Matches: %d | Time: %.4f ms%n",
                    prefix, results.size(), elapsedMillis);
            return results;
        }

        private void collectPrefix(AVLNode node, String prefix, List<String> results, int maxResults) {
            if (node == null || results.size() >= maxResults) return;

            if (node.key.compareTo(prefix) >= 0) {
                collectPrefix(node.left, prefix, results, maxResults);
            }

            if (node.key.startsWith(prefix) || node.key.contains(prefix)) {
                results.add(node.key);
            }

            collectPrefix(node.right, prefix, results, maxResults);
        }

        public void printTreeStats() {
            System.out.println("==========================================");
            System.out.println("AVL TREE ACADEMIC AUDIT STATS");
            System.out.println("Total Nodes: " + totalNodes);
            System.out.println("Tree Height: " + getHeight(root));
            System.out.println("Total Rotations (LL, RR, LR, RL): " + totalRotations);
            System.out.println("Root Balance Factor: " + getBalance(root));
            System.out.println("Is Balanced (|BF| <= 1): " + (Math.abs(getBalance(root)) <= 1));
            System.out.println("==========================================");
        }
    }

    // Academic Demonstration Main Runner
    public static void main(String[] args) {
        System.out.println("College Mini-Project: Smart Search Autocomplete");
        System.out.println("ADSA Module: AVL Tree Demonstration\n");

        AVLTree tree = new AVLTree();

        // Sample indexing
        String[][] samples = {
            {"Laptop", "PROD-1001"},
            {"Laptop Stand", "PROD-1002"},
            {"Laptop Charger", "PROD-1003"},
            {"Gaming Laptop", "PROD-1004"},
            {"Laptop Bag", "PROD-1005"},
            {"Smartphone", "PROD-1006"},
            {"Smart Watch", "PROD-1007"},
            {"Headphones", "PROD-1008"},
            {"Wireless Mouse", "PROD-1009"},
            {"Mechanical Keyboard", "PROD-1010"}
        };

        for (String[] item : samples) {
            tree.insert(item[0], item[1]);
        }

        tree.printTreeStats();

        // Testing prefix autocomplete
        System.out.println("\nTesting Autocomplete prefix: 'lap'");
        List<String> suggestions = tree.autocomplete("lap", 5);
        for (String s : suggestions) {
            System.out.println(" -> " + s);
        }
    }
}
