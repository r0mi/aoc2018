import os
import string
import functools
import operator

base_file = os.path.splitext(__file__)[0]

polymer = ""

with open(base_file + ".input", "r") as fo:
	polymer = fo.read().rstrip();

react_list = functools.reduce(operator.iconcat, list(map(lambda x: [x[0]+x[1],x[1]+x[0]], zip(string.ascii_lowercase, string.ascii_uppercase))))

def react(polymer):
	reacted = True
	while reacted:
		len_before_reaction = len(polymer)
		for replace in react_list:
			polymer = polymer.replace(replace, "")

		if len(polymer) == len_before_reaction:
			reacted = False
	return (len(polymer), polymer)

reacted_len, reacted_polymer = react(polymer)

print("Units after initial reaction", reacted_len)

shortest_polymer = reacted_len
shortest_polymer_unit = ""

for c in string.ascii_lowercase:
	improved_polymer = reacted_polymer.replace(c, "").replace(c.upper(), "")
	improved_reacted_length, improved_reacted_polymer = react(improved_polymer)

	if improved_reacted_length < shortest_polymer:
		shortest_polymer = improved_reacted_length
		shortest_polymer_unit = "%c/%c" % (c.upper(), c)

print("Shortest polymer", shortest_polymer, "after removing all", shortest_polymer_unit, "units")
