# AVL Tree
Implementation of a balanced binary tree in Python.

 Course: Data Structures

## Assignment instructions:

Implement a balanced AVL tree.
Each node in the tree has a value (info) and a key, which is an integer. All keys are different, and the order of nodes is in relation to the keys.

Implement the following functions:
* search(k): The function searches for a node with a key k. Returns a pointer to the node if it exists, and None otherwise.
* insert(k, v): Inserts a node with value v and key k. Assume the key is not already in the tree. Returns the number of rotations needed to preserve the tree's balance.
* delete(x): Given a pointer, delete the node x. Returns the number of rotations needed to preserve the tree's balance.
* avl_to_array(): Returns a sorted array (by keys) of the nodes in the tree, when each node is represented by (key, value).
* size(): Returns the number of nodes in the tree.
* split(x): Receives a pointer to a node x, and seperates the tree into 2 AVL trees, when the first's keys are lower than x's, and the other's are higher. After calling the function, x is unusable.
* join(t, k, v): Receives another tree t with keys lower than the current tree, when k is between them. The function joins the 2 trees into 1, with the new node (k, v). Returns the "cost" (balance factor + 1). After calling the function, t is unusable.
* get_root(): Returns a pointer to the root.

In addition, implement the AVLNode class.

For convenience sake, each leaf should have 2 "virtual" sons (nodes without a key).