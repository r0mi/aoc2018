import os
import re
import sys
from math import log, floor

base_file = os.path.splitext(__file__)[0]

regex = re.compile(r"pos=<(?P<pos>[0-9-,]+)>, r=(?P<r>\d+)")

nanobots = []

with open(base_file + ".input", "r") as fo:
	for line in fo:
		match = regex.search(line.rstrip())

		if match:
			if match.group("pos"):
				nanobots.append((tuple(map(int, match.group("pos").split(","))), int(match.group("r"))))

nanobots.sort(key=lambda x: x[1], reverse=True)

main_nanobot = nanobots[0]

def manhattan_distance(a, b):
	x1, y1, z1 = a
	x2, y2, z2 = b

	return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)

in_range_of_main_bot = []

for bot in nanobots:
	if manhattan_distance(main_nanobot[0], bot[0]) <= main_nanobot[1]:
		in_range_of_main_bot.append(bot)

print("%u nanobots are in range of the nanobot with the largest signal radius" % len(in_range_of_main_bot))

min_x = min(nanobots, key=lambda bot: bot[0][0])[0][0]
max_x = max(nanobots, key=lambda bot: bot[0][0])[0][0]
min_y = min(nanobots, key=lambda bot: bot[0][1])[0][1]
max_y = max(nanobots, key=lambda bot: bot[0][1])[0][1]
min_z = min(nanobots, key=lambda bot: bot[0][2])[0][2]
max_z = max(nanobots, key=lambda bot: bot[0][2])[0][2]

min_dim = min([max_x - min_x, max_y - min_y, max_z - min_z])
step = pow(10, floor(log(min_dim, 10)))

max_in_range = -1
max_in_range_coords = []

new_bots = []

while True:
	# print("Step %d: %d <= x <= %d; %d <= y <= %d; %d <= z <= %d" % (step, min_x, max_x, min_y, max_y, min_z, max_z))

	for x in range(min_x, max_x + 1, step):
		for y in range(min_y, max_y + 1, step):
			for z in range(min_z, max_z + 1, step):
				current_position = (x, y, z)
				num_in_range = 0
				bots_in_range = []

				for bot in nanobots:
					if manhattan_distance(bot[0], current_position) <= bot[1]:
						num_in_range += 1

				if num_in_range > max_in_range:
					# print("%d in range" % (num_in_range))
					max_in_range = num_in_range
					max_in_range_coords = [current_position]

				elif num_in_range == max_in_range:
					max_in_range_coords.append(current_position)

	if step == 1:
		closest = sys.maxsize
		position = None

		for coords in max_in_range_coords:
			if sum(coords) < closest:
				closest = sum(coords)
				position = coords

		print("Closest point to (0,0,0) that is in range of most nanobots (%u) is %s with a manhattan distance of %u" % (max_in_range, str(position), closest))
		break
	else:
		closest = sys.maxsize
		position = None

		for coords in max_in_range_coords:
			if sum(coords) < closest:
				closest = sum(coords)
				position = coords

		# print("Next center position", position)
		min_x = position[0] - step
		max_x = position[0] + step
		min_y = position[1] - step
		max_y = position[1] + step
		min_z = position[2] - step
		max_z = position[2] + step

		step = step // 10
