import os

base_file = os.path.splitext(__file__)[0]

license = []

with open(base_file + ".input", "r") as fo:
	license = map(int, fo.read().rstrip().split());

class Node:
	def __init__(self):
		self.children = []
		self.missing_childs = 0
		self.metadata = []
		self.missing_metadata_elements = 0
		self.parent = None

	def add_metadata(self, metadata):
		self.missing_metadata_elements = self.missing_metadata_elements - 1
		self.metadata.append(metadata)

	def add_child(self, child):
		self.missing_childs = self.missing_childs - 1
		self.children.append(child)

	def missing_metadata(self):
		return self.missing_metadata_elements > 0

	def missing_children(self):
		return self.missing_childs > 0


# Read states
# 0 - number of node
# 1 - number of meta
# 2 - child node start
# 3 - meta for current node

state = 0
current_element = None
current_master = None
master_stack = []

for entry in license:
	if state == 0:
		current_element = Node()
		current_element.missing_childs = entry
		state = state + 1

	elif state == 1:
		current_element.missing_metadata_elements = entry

		if current_element.missing_childs:
			state = state + 1
		else:
			state = 3

	elif state == 2:
		if current_master:
			master_stack.append(current_master)

		current_master = current_element
		current_element = Node()
		current_element.missing_childs = entry
		current_element.parent = current_master
		current_master.add_child(current_element)
		state = 1

	elif state == 3:
		current_element.add_metadata(entry)

		if not current_element.missing_metadata():
			if current_element.parent and current_element.parent.missing_children():
				current_element = current_master
				current_master = master_stack.pop() if master_stack else None
				state = 2

			elif current_element.parent and current_element.parent.missing_metadata():
				current_element = current_master
				current_master = master_stack.pop() if master_stack else None
				state = 3


def calculate_checksum(checksum, node):
	checksum = checksum + sum(node.metadata)
	for child in node.children:
		checksum = calculate_checksum(checksum, child)
	return checksum


def calculate_child_value(node):
	value = 0
	if len(node.children) == 0:
		return sum(node.metadata)
	else:
		for metadata in node.metadata:
			if metadata != 0 and metadata <= len(node.children):
				value = value + calculate_child_value(node.children[metadata - 1])
	return value

print("Sum of all metadata entries is", calculate_checksum(0, current_element))

print("Value of root node is", calculate_child_value(current_element))
