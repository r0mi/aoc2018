import os
import re

GENERATION_COUNT_1 = 20
GENERATION_COUNT_2 = 50000000000
RULE_LENGTH = 5

base_file = os.path.splitext(__file__)[0]

regex = re.compile(r"initial state: (?P<initial>[#.]*)|^.{0}$|(?P<rule>[#.]{5}) => (?P<result>[.#])")

initial_state = ""
grow_rules = []

with open(base_file + ".input", "r") as fo:
	for line in fo:
		match = regex.search(line.rstrip())
		if match:
			if match.group("initial"):
				initial_state = match.group("initial")
			elif match.group("rule") and match.group("result") == "#":
				grow_rules.append(match.group("rule"))

def adjust_state(zero_index, state):
	index = 0

	if state.index("#") < RULE_LENGTH - 1:
		index = 4 - state.index("#")
		state = "." * (RULE_LENGTH - 1 - state.index("#")) + state

	if state.rindex("#") > len(state) - RULE_LENGTH:
		state = state + "." * (state.rindex("#") - len(state) + RULE_LENGTH)

	return (zero_index - index, state)


def sum_plant_pot_numbers(index, state):
	total = 0

	for i, pot in enumerate(state):
		if pot == "#":
			total = total + i + index

	return total


def simulate_generations(generation_count, initial_index, initial_state):
	fo = open(base_file + ".output", "w")
	fo.write("%3d: %s\n" % (0, initial_state))

	previous_index = initial_index
	previous_state = initial_state
	previous_sum = sum_plant_pot_numbers(initial_index, initial_state)
	sum_diff = 0
	generation_index = 1

	while True:
		new_state = ".."

		for x in range(len(previous_state) + 1 - RULE_LENGTH):
			if previous_state[x: x + 5] in grow_rules:
				new_state = new_state + "#"
			else:
				new_state = new_state + "."

		new_index, new_state = adjust_state(previous_index, new_state)
		new_sum = sum_plant_pot_numbers(new_index, new_state)
		sum_diff = new_sum - previous_sum
		previous_sum = new_sum

		fo.write("%3d: %s\n" % (generation_index, new_state))

		if previous_state.strip(".") == new_state.strip(".") or generation_index == generation_count:
			fo.write("Repeating pattern with sum increase of %d\n" % sum_diff)
			break

		previous_state = new_state
		generation_index += 1

	total = previous_sum + (generation_count - generation_index) * sum_diff

	print("Total plants after %d generations is %d" % (generation_count, total))
	fo.close()


initial_index = -1 * RULE_LENGTH
initial_state = "." * RULE_LENGTH + initial_state + "." * RULE_LENGTH

for generation_count in [GENERATION_COUNT_1, GENERATION_COUNT_2]:
	simulate_generations(generation_count, initial_index, initial_state)

