"""A class represnting a node in an AVL tree"""
class AVLNode(object):
	"""Constructor, you are allowed to add more fields.

	@type key: int or None
	@type value: any
	@param value: data of your node
	"""
	def __init__(self, key, value):
		self.key = key
		self.value = value
		self.left = None
		self.right = None
		self.parent = None
		self.height = -1
		self.size = 0

# AVLNode functions
	"""returns the left child
	@rtype: AVLNode
	@returns: the left child of self, None if there is no left child (if self is virtual)
	"""
	def get_left(self):
		return self.left

	"""returns the right child

	@rtype: AVLNode
	@returns: the right child of self, None if there is no right child (if self is virtual)
	"""
	def get_right(self):
		return self.right

	"""returns the parent 

	@rtype: AVLNode
	@returns: the parent of self, None if there is no parent
	"""
	def get_parent(self):
		return self.parent

	"""returns the key

	@rtype: int or None
	@returns: the key of self, None if the node is virtual
	"""
	def get_key(self):
		return self.key

	"""returns the value

	@rtype: any
	@returns: the value of self, None if the node is virtual
	"""
	def get_value(self):
		return self.value

	"""returns the height

	@rtype: int
	@returns: the height of self, -1 if the node is virtual
	"""
	def get_height(self):
		return self.height

	"""returns the sub tree size of the node

	@rtype: int
	@returns: the size of self, 0 if the node is virtual
	"""
	def get_size(self):
		return self.size

	"""returns the balance factor of the node
	
	@pre: node is a real node
	@rtype: int
	@returns: balance factor if node
	"""
	def get_bf(self):  # Calculates node's balance factor, O(1)
		return self.get_left().get_height() - self.get_right().get_height()

	"""sets left child

	@type node: AVLNode
	@param node: a node
	"""
	def set_left(self, node):
		self.left = node

	"""sets right child

	@type node: AVLNode
	@param node: a node
	"""
	def set_right(self, node):
		self.right = node

	"""sets parent

	@type node: AVLNode
	@param node: a node
	"""
	def set_parent(self, node):
		self.parent = node

	"""sets key

	@type key: int or None
	@param key: key
	"""
	def set_key(self, key):
		self.key = key

	"""sets value

	@type value: any
	@param value: data
	"""
	def set_value(self, value):
		self.value = value

	"""sets the height of the node

	@type h: int
	@param h: the height
	"""
	def set_height(self, h):
		self.height = h

	"""sets the size of the node

	@type s: int
	@param s: the size
	"""
	def set_size(self, s):
		self.size = s

	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def is_real_node(self):
		return self.key is not None


"""
A class implementing the ADT Dictionary, using an AVL tree.
"""
class AVLTree(object):

	def __init__(self):  # Initializes an empty tree, O(1)
		self.root = None

	"""searches for a AVLNode in the dictionary corresponding to the key

	@type key: int
	@param key: a key to be searched
	@rtype: AVLNode
	@returns: the AVLNode corresponding to key or None if key is not found.
	"""
	def search(self, key):  # Searches for a node with key="key" in self, O(log(n))
		node = self.root
		while node.is_real_node():
			if node.get_key() == key:
				return node
			if key < node.get_key():
				node = node.get_left()
			else:
				node = node.get_right()
		return None

	def rotate_right(self, b):  # Rotates nodes to the right, O(1)
		if self.root.get_key() == b.get_key():  # if rotation is at root, then set the new root
			self.root = b.get_left()

		a = b.get_left()
		b.set_left(a.get_right())
		b.get_left().set_parent(b)
		a.set_right(b)
		a.set_parent(b.get_parent())
		if a.get_parent() is not None:
			if a.get_parent().get_key() < a.get_key():
				a.get_parent().set_right(a)
			else:
				a.get_parent().set_left(a)
		b.set_parent(a)

		# update height and size of a and b
		b.set_height(max(b.get_left().get_height(), b.get_right().get_height()) + 1)
		b.set_size(b.get_left().get_size() + b.get_right().get_size() +1)
		a.set_height(max(a.get_left().get_height(), a.get_right().get_height()) + 1)
		a.set_size(a.get_left().get_size() + a.get_right().get_size() + 1)

	def rotate_left(self, b):  # Rotates nodes to the left, O(1)
		if self.root.get_key() == b.get_key():  # if rotation is at root, then set the new root
			self.root = b.get_right()

		a = b.get_right()
		b.set_right(a.get_left())
		b.get_right().set_parent(b)
		a.set_left(b)
		a.set_parent(b.get_parent())
		if a.get_parent() is not None:
			if a.get_parent().get_key() < a.get_key():
				a.get_parent().set_right(a)
			else:
				a.get_parent().set_left(a)
		b.set_parent(a)

		# update height and size of a and b
		b.set_height(max(b.get_left().get_height(), b.get_right().get_height()) + 1)
		b.set_size(b.get_left().get_size() + b.get_right().get_size() + 1)
		a.set_height(max(a.get_left().get_height(), a.get_right().get_height()) + 1)
		a.set_size(a.get_left().get_size() + a.get_right().get_size() + 1)

	@staticmethod
	#  USE THIS FOR INSERTIONS ONLY - UPDATES NODES SIZES ASSUMING INSERTION!
	def tree_position_insert(node, key):  # returns parent of node with key 'key', in node's subtree + update size of nodes, O(log n)
		while node.is_real_node():
			parent = node
			if key < node.get_key():
				node = node.get_left()
			else:
				node = node.get_right()
			parent.set_size(parent.get_size() + 1)
		return parent

	def tree_insert(self, starthere, node):  # finds node's parent. Insert node as parent's child, O(log n)
		parent = self.tree_position_insert(starthere, node.get_key())
		node.set_parent(parent)
		if node.get_key() < parent.get_key():
			parent.set_left(node)
		else:
			parent.set_right(node)

	"""inserts val at position i in the dictionary

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: any
	@param val: the value of the item
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def insert(self, key, val):  # Insert new node into self, O(log n)
		cnt_balance = 0

		new_node = AVLNode(key, val)  # Create new AVLNode with virtual children
		new_node.set_left(AVLNode(None, None))
		new_node.get_left().set_parent(new_node)
		new_node.set_right(AVLNode(None, None))
		new_node.get_right().set_parent(new_node)
		new_node.set_height(0)
		new_node.set_size(1)

		if self.root is None:  # Tree is empty
			self.root = new_node  # insert_me is root of tree
			self.root.set_height(0)
			self.root.set_size(1)
			return cnt_balance  # No rotations were necessary - no rotations were made
		else:  # insertion as seen in lecture (using the same methods)
			self.tree_insert(self.root, new_node)

		# Rotations:
		parent = new_node.get_parent()
		while parent is not None:  # We don't set a virtual parent, so trying to access root's parent we get None
			bf = parent.get_bf()  # parent's balance factor
			prev_height = parent.get_height()
			parent.set_height(max(parent.get_left().get_height(), parent.get_right().get_height()) + 1)
			if abs(bf) < 2:
				if parent.get_height() == prev_height:
					return cnt_balance
				else:  # parent's height changed
					cnt_balance += 1  # Updating height counts as a balancing act
					parent = parent.get_parent()
			else:  # |BF|==2
				if bf == -2:
					cnt_balance += 1
					if parent.get_right().get_bf() == -1:
						self.rotate_left(parent)
					else:
						cnt_balance += 1
						self.rotate_right(parent.get_right())
						self.rotate_left(parent)
				else:  # BF==2
					cnt_balance += 1
					if parent.get_left().get_bf() == 1:
						self.rotate_right(parent)
					else:
						cnt_balance += 1
						self.rotate_left(parent.get_left())
						self.rotate_right(parent)
				parent.set_height(max(parent.get_left().get_height(), parent.get_right().get_height()) + 1)
		return cnt_balance  # no need to check "deeper" parents - lecture concluded that one rotation at most is needed

	@staticmethod
	def min(node):  # get the node with minimal key in node's subtree, O(log n)
		while node.get_left().is_real_node():
			node = node.get_left()
		return node

	def successor(self, node):  # get the successor of node, O(log n)
		if node.get_right().is_real_node():
			return self.min(node.get_right())
		parent = node.get_parent()
		while parent is not None and node.get_key() == parent.get_right().get_key():
			node = parent
			parent = node.get_parent()
		return parent

	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def delete(self, node):  # Deletes a node from self, O(log n)
		cnt_balance = 0
		parent = node.get_parent()

		if node.get_size() == 1:  # node is a leaf
			if node.get_key() == self.get_root().get_key():  # Tree has only this node and it's the root
				self.root = None
			elif node.get_key() < parent.get_key():
				parent.set_left(AVLNode(None, None))
				parent.get_left().set_parent(parent)
			else:
				parent.set_right(AVLNode(None, None))
				parent.get_right().set_parent(parent)
		elif not node.get_left().is_real_node() and node.get_right().is_real_node():  # node has only right child
			if node.get_key() == self.get_root().get_key():  # Delete root that has only right child
				self.root = node.get_right()
				self.get_root().set_parent(None)
			elif node.get_key() < parent.get_key():
				parent.set_left(node.get_right())
				parent.get_left().set_parent(parent)
			else:
				parent.set_right(node.get_right())
				parent.get_right().set_parent(parent)
		elif node.get_left().is_real_node() and not node.get_right().is_real_node():  # node has only  left child
			if node.get_key() == self.get_root().get_key():  # Delete root that has only left child
				self.root = node.get_left()
				self.get_root().set_parent(None)
			elif node.get_key() < parent.get_key():
				parent.set_left(node.get_left())
				parent.get_left().set_parent(parent)
			else:
				parent.set_right(node.get_left())
				parent.get_right().set_parent(parent)
		else:  # Node has 2 children
			succ = self.successor(node)  # Remove successor from the tree
			parent = succ.get_parent()  # Save successor's parent, for later rotations
			if parent.get_key() == node.get_key():  # The successor is the child of node
				succ.set_left(node.get_left())
				succ.get_left().set_parent(succ)
				succ.set_parent(node.get_parent())
				parent = succ
			else:
				parent.set_left(succ.get_right())
				parent.get_left().set_parent(parent)
				succ.set_parent(node.get_parent())  # Insert successor in node's position
				succ.set_left(node.get_left())
				succ.set_right(node.get_right())
				succ.get_left().set_parent(succ)  # Detach node from tree
				succ.get_right().set_parent(succ)
			if succ.get_parent() is not None:  # node had a real parent, else it was the root
				if succ.get_key() < succ.get_parent().get_key():
					succ.get_parent().set_left(succ)
				else:
					succ.get_parent().set_right(succ)
			else:
				self.root = succ

		# Rotations + updates
		while parent is not None:  # We don't set a virtual parent, so trying to access root's parent we get None
			bf = parent.get_bf()  # parent's balance factor
			prev_height = parent.get_height()
			parent.set_size(parent.get_left().get_size() + parent.get_right().get_size() +1)
			parent.set_height(max(parent.get_left().get_height(), parent.get_right().get_height()) + 1)
			if abs(bf) < 2:
				if parent.get_height() != prev_height:  # Algorithm from lecture, line 3.3 (parent's height changed)
					cnt_balance += 1  # Updating height counts as a balancing act, as instructed in course forum
			else:  # Algorithm from lecture, line 3.4 (|BF|==2)
				if bf == -2:
					cnt_balance += 1
					if parent.get_right().get_bf() == -1 or parent.get_right().get_bf() == 0:
						self.rotate_left(parent)
					else:
						cnt_balance += 1
						self.rotate_right(parent.get_right())
						self.rotate_left(parent)
				else:  # BF==2
					cnt_balance += 1
					if parent.get_left().get_bf() == 1 or parent.get_left().get_bf() == 0:
						self.rotate_right(parent)
					else:
						cnt_balance += 1
						self.rotate_left(parent.get_left())
						self.rotate_right(parent)
			parent = parent.get_parent()
		return cnt_balance

	def rec_add_to_array_in_order(self, node, array):  # Creates a sorted array based on keys with self's nodes, O(n)
		if node.is_real_node():
			self.rec_add_to_array_in_order(node.get_left(), array)
			array.append((node.get_key(), node.get_value()))  # O(1)
			self.rec_add_to_array_in_order(node.get_right(), array)

	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self):  # Returns a sorted array based on keys with self's nodes, O(n)
		sorted_array = []
		if self.root is not None:
			self.rec_add_to_array_in_order(self.root, sorted_array)  # O(n)
		return sorted_array

	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""
	def size(self):  # Returns the size of self, O(1)
		if self.root is None:
			return 0
		return self.root.get_size()

	"""splits the dictionary at the i'th index

	@type node: AVLNode
	@pre: node is in self
	@param node: The intended node in the dictionary according to whom we split
	@rtype: list
	@returns: a list [left, right], where left is an AVLTree representing the keys in the 
	dictionary smaller than node.key, right is an AVLTree representing the keys in the 
	dictionary larger than node.key.
	"""
	def split(self, node):  # Splits a tree to 2 trees as explained in the contract, O(log n)
		small_tree = AVLTree()
		big_tree = AVLTree()
		temp_tree = AVLTree()
		if node.get_left().is_real_node():
			small_tree.root = node.get_left()
			small_tree.get_root().set_parent(None)
		if node.get_right().is_real_node():
			big_tree.root = node.get_right()
			big_tree.get_root().set_parent(None)

		parent = node.get_parent()
		while parent is not None:
			temp_parent = parent.get_parent()
			if parent.get_key() < node.get_key():
				temp_tree.root = parent.get_left()
				temp_tree.get_root().set_parent(None)
				small_tree.join(temp_tree, parent.get_key(), parent.get_value())
			else:
				temp_tree.root = parent.get_right()
				temp_tree.get_root().set_parent(None)
				big_tree.join(temp_tree, parent.get_key(), parent.get_value())
			parent = temp_parent

		return [small_tree, big_tree]


	"""joins self with key and another AVLTree

	@type tree2: AVLTree 
	@param tree2: a dictionary to be joined with self
	@type key: int 
	@param key: The key separting self with tree2
	@type val: any 
	@param val: The value attached to key
	@pre: all keys in self are smaller than key and all keys in tree2 are larger than key
	@rtype: int
	@returns: the absolute value of the difference between the height of the AVL trees joined
	"""
	def join(self, tree2, key, val):  # Joins 2 AVL trees with a new node (key, val) (see contract), O(log n)
		# SpEciAl Cases:
		if self.size() == 0:  # self is an empty tree
			if tree2.size() == 0:  # tree2 is also empty
				self.insert(key, val)
				return 1
			else:
				self.root = tree2.get_root()
				self.insert(key, val)
				return tree2.get_root().get_height() + 2  # self's height is -1
		elif tree2.size() == 0:  # self isn't empty, but tree2 is
			self.insert(key, val)
			return self.get_root().get_height() + 2  # tree2's height is -1
		h1 = self.get_root().get_height()
		h2 = tree2.get_root().get_height()
		if self.size() == 1:  # self is a leaf with height of 0
			tree2.insert(key, val)
			tree2.insert(self.get_root().get_key(), self.get_root().get_value())
			self.root = tree2.get_root()
			return h2 + 1
		elif tree2.size() == 1:  # tree2 is a leaf with height 0
			self.insert(key, val)
			self.insert(tree2.get_root().get_key(), tree2.get_root().get_value())
			return h1 + 1

		# self and tree2 aren't empty or leaves
		if self.get_root().get_key() > tree2.get_root().get_key():
			root1 = self.get_root()
			root2 = tree2.get_root()
			self.root = root2
			tree2.root = root1
		h1 = self.get_root().get_height()
		h2 = tree2.get_root().get_height()
		middle_node = AVLNode(key, val)
		cost = abs(h1-h2) + 1
		if h1 <= h2:
			b = tree2.get_root()
			while b.get_height() >= h1:
				b = b.get_left()
			c = b.get_parent()
			#  Pointers substitutions
			self.get_root().set_parent(middle_node)
			b.set_parent(middle_node)
			middle_node.set_left(self.get_root())
			middle_node.set_right(b)
			middle_node.set_parent(c)
			c.set_left(middle_node)
			self.root = tree2.get_root()
		else:
			b = self.get_root()
			while b.get_height() > h2:
				b = b.get_right()
			c = b.get_parent()
			# Pointers substitutions
			tree2.get_root().set_parent(middle_node)
			b.set_parent(middle_node)
			middle_node.set_left(b)
			middle_node.set_right(tree2.get_root())
			middle_node.set_parent(c)
			c.set_right(middle_node)
		# Rotations
		fix_me = middle_node
		while fix_me is not None:  # We don't set a virtual parent, so trying to access root's parent we get None
			bf = fix_me.get_bf()  # parent's balance factor
			prev_height = fix_me.get_height()
			fix_me.set_height(max(fix_me.get_left().get_height(), fix_me.get_right().get_height()) + 1)
			fix_me.set_size(fix_me.get_left().get_size() + fix_me.get_right().get_size() + 1)
			if abs(bf)<2:
				fix_me = fix_me.get_parent()
				continue
			if bf == -2:
				if fix_me.get_right().get_bf() == -1 or fix_me.get_right().get_bf() == 0:
					self.rotate_left(fix_me)
				else:
					self.rotate_right(fix_me.get_right())
					self.rotate_left(fix_me)
			else:  # BF==2
				if fix_me.get_left().get_bf() == 1 or fix_me.get_left().get_bf() == 0:
					self.rotate_right(fix_me)
				else:
					self.rotate_left(fix_me.get_left())
					self.rotate_right(fix_me)
			fix_me = fix_me.get_parent()

		return cost


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):  # Returns the root of the tree "self", O(1)
		return self.root

