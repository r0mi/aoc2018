import os
from collections import defaultdict

NUM_DOORS_TO_PASS = 1000

base_file = os.path.splitext(__file__)[0]

directions = ""

delta = {
    "N": ( 0, -1),
    "E": ( 1,  0),
    "S": ( 0,  1),
    "W": (-1,  0)
}

with open(base_file + ".input", "r") as fo:
	directions = fo.read().strip("^$")


def find_end_of_branch(source, start):
	i = start
	n = 0

	while i < len(source):
		if n == 0 and source[i] == "|":
			break

		elif source[i] == "(":
			n += 1

		elif source[i] == ")":
			n -= 1

		i += 1

	return i


def get_branches(source, start):
	branches = []
	i = start + 1
	branch_start = i
	n = 1

	while i < len(source):
		if source[i] == "(":
			n += 1

		elif source[i] == ")":
			n -= 1

		elif n == 1 and source[i] == "|":
			# lookahead

			if source[i + 1] == ")":
				branches.append(source[branch_start:branch_start + (i - branch_start) // 2])

			else:
				branches.append(source[branch_start:i])

			branch_start = i + 1

		if n == 0:
			if branch_start != i:
				branches.append(source[branch_start:i])
				i += 1
				break

			else:
				branch_start = i + 1
				eob = find_end_of_branch(source, branch_start)
				branches.append(source[branch_start:eob])
				i = eob
				break

		i += 1

	assert n == 0

	return (i, branches)



def parse_directions(prefix, paths, directions):
	current_path = prefix
	i = 0

	while i < len(directions):

		if directions[i] not in "(|)":
			current_path += directions[i]
		elif directions[i] == "(":
			end, branches = get_branches(directions, i)

			for branch in branches:
				paths = parse_directions(current_path, paths, branch)

			i = end

			if i >= len(directions):
				return paths

		i += 1

	paths.append(current_path)

	return paths



paths = parse_directions("", [], directions)
paths.sort(key=lambda x: len(x), reverse=True)

print("The largest number of doors needed to pass to reach a room is", len(paths[0]))

longest_paths = filter(lambda x: len(x) >= NUM_DOORS_TO_PASS, paths)
room_distances = defaultdict(int)
room_distances[(0, 0)] = 1000

for path in longest_paths:
	x = prev_x = 0
	y = prev_y = 0

	for c in path[NUM_DOORS_TO_PASS:]:
		dx, dy = delta[c]
		x += dx
		y += dy

		if room_distances[(x, y)] != 0:
			room_distances[(x, y)] = min(room_distances[(x, y)], room_distances[(prev_x, prev_y)] + 1)

		else:
			room_distances[(x, y)] = room_distances[(prev_x, prev_y)] + 1

		prev_x = x
		prev_y = y

print("%u rooms have a shortest path of at least %u doors" % (len([x for x in room_distances.values() if x >= NUM_DOORS_TO_PASS]), NUM_DOORS_TO_PASS))

