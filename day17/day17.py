import os
import re

base_file = os.path.splitext(__file__)[0]

regex = re.compile(r"x=(?P<x>\d+), y=(?P<y_from>\d+)..(?P<y_to>\d+)|y=(?P<y>\d+), x=(?P<x_from>\d+)..(?P<x_to>\d+)")

sand = "."
clay = "#"
still_water = "~"
moving_water = "|"

min_x = 500
max_x = 0
min_y = 500
max_y = 0

spring = [500, 0]
clay_tiles = set()

with open(base_file + ".input", "r") as fo:
	for line in fo:
		match = regex.search(line.rstrip())

		if match:
			if match.group("x"):
				x = int(match.group("x"))
				y_from = int(match.group("y_from"))
				y_to = int(match.group("y_to"))

				if x < min_x:
					min_x = x
				elif x > max_x:
					max_x = x

				if y_to > max_y:
					max_y = y_to

				if y_from < min_y:
					min_y = y_from

				for y in range(y_from, y_to + 1):
					clay_tiles.add((x, y))
			else:
				y = int(match.group("y"))
				x_from = int(match.group("x_from"))
				x_to = int(match.group("x_to"))

				if x_from < min_x:
					min_x = x_from

				if x_to > max_x:
					max_x = x_to

				if y > max_y:
					max_y = y
				elif y < min_y:
					min_y = y

				for x in range(x_from, x_to + 1):
					clay_tiles.add((x, y))


def write_map(u_map, suffix=""):
	with open(base_file + suffix + ".output", "w+") as fo:
		for y in range(len(underground_map)):
			fo.write("%4d " % y)

			for x in range(len(underground_map[y])):
				fo.write(underground_map[y][x])

			fo.write('\n')


def find_bottom(source, u_map):
	x = source[0]
	y = source[1]
	bottom = ''

	while bottom not in ['#', still_water] and y < max_y:
		y += 1
		bottom = u_map[y][x]

	if y == max_y:
		return None

	return y - 1


def find_reservoir_sides(point, u_map):
	X = point[0]
	Y = point[1]
	left = None
	right = None

	for x in range(X - 1, 0, -1):
		if u_map[Y][x] == clay:
			left = x + 1
			break

		elif u_map[Y + 1][x] == sand:
			left = None
			break

	for x in range(X + 1, map_width):
		if u_map[Y][x] == clay:
			right = x - 1
			break

		elif u_map[Y + 1][x] == sand:
			right = None
			break

	return (left, right)


def find_overflow_points(point, u_map):
	X = point[0]
	Y = point[1]
	left = None
	right = None

	for x in range(X - 1, -1, -1):
		if u_map[Y][x] == clay:
			left = (x + 1, False)
			break

		elif u_map[Y][x] == moving_water and u_map[Y + 1][x] == moving_water:
			left = None
			break

		elif u_map[Y + 1][x] == sand:
			left = (x, True)
			break

		elif u_map[Y + 1][x] == moving_water:
			left = None
			break

	for x in range(X + 1, map_width):
		if u_map[Y][x] == clay:
			right = (x - 1, False)
			break

		elif u_map[Y][x] == moving_water and u_map[Y + 1][x] == moving_water:
			right = None
			break

		elif u_map[Y + 1][x] == sand:
			right = (x, True)
			break

		elif u_map[Y + 1][x] == moving_water:
			right = None
			break

	return (left, right)


def fill_reservoir(source, u_map):
	X = source[0]
	y = source[1]

	left, right = find_reservoir_sides(source, u_map)

	while left and right and y > 0:
		for x in range(left, right + 1):
			u_map[y][x] = still_water

		y -= 1
		left, right = find_reservoir_sides((X, y), u_map)

	return y


def fill_overflow(source, u_map):
	X = source[0]
	Y = source[1]

	left, right = find_overflow_points(source, u_map)

	if left and right:
		for x in range(left[0], right[0] + 1):
			u_map[y][x] = moving_water

		if left[1] and right[1]:
			return [(left[0], Y), (right[0], Y)]
		elif left[1]:
			return [(left[0], Y)]
		elif right[1]:
			return [(right[0], Y)]
	else:
		return []


def fill_fall(source, dest, u_map):
	X = source[0]

	for y in range(max(source[1] + 1, min_y), dest[1] + 1):
		u_map[y][X] = moving_water


min_x -= 1
max_x += 1
max_y += 1
underground_map = [[sand for x in range(min_x, max_x + 1)] for y in range(max_y + 1)]
map_width = len(underground_map[0])
map_heigth = len(underground_map)
underground_map[spring[1]][spring[0] - min_x] = '+'
spring[0] -= min_x

for y in range(max_y + 1):
	for x in range(min_x, max_x + 1):
		if (x, y) in clay_tiles:
			underground_map[y][x - min_x] = clay

write_map(underground_map, "_empty")

sources = [spring]
processed_sources = set(spring)
tiles = 0

while sources:
	source = sources.pop(0)
	x = source[0]
	y = find_bottom(source, underground_map)

	if y:
		y = fill_reservoir((x, y), underground_map)
		overflow_points = fill_overflow((x, y), underground_map)

		if overflow_points:
			for overflow_point in overflow_points:
				if overflow_point not in processed_sources:
					sources.append(overflow_point)
					processed_sources.add(overflow_point[:])

		fill_fall(source, (x, y - 1), underground_map)
	else:
		fill_fall(source, (x, max_y - 1), underground_map)


write_map(underground_map, "_filled")

tiles_still = 0
tiles_moving = 0
for y in range(len(underground_map)):
	for x in range(len(underground_map[y])):
		if underground_map[y][x] == moving_water:
			tiles_moving += 1
		elif underground_map[y][x] == still_water:
			tiles_still += 1

print("The water can reach %u tiles" % (tiles_still + tiles_moving))
print("After water spring stops producing water %u tiles are left" % tiles_still)

