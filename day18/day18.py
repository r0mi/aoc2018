import os
import hashlib
from copy import deepcopy

base_file = os.path.splitext(__file__)[0]

FIRST_RESULT_MINUTE = 10
SECOND_RESULT_MINUTE = 1000000000

wooded = "|"
open_ground = "."
lumberyard = "#"

lumber_area_size = 50
landscape = []

col_num = [-1,  0,  1, -1, 1, -1, 0, 1]
row_num = [-1, -1, -1,  0, 0,  1, 1, 1]

with open(base_file + ".input", "r") as fo:
	for line in fo:
		landscape.append(list(line.rstrip()))


def print_map(minute, landscape):
	os.system("clear")
	print("Minute #%u, value %u" % (minute, resource_value(landscape)))

	for y in range(lumber_area_size):
		for x in range(lumber_area_size):
			print(landscape[y][x], end="")

		print()


def flatten_landscape(landscape):
	return "".join([x for y in landscape for x in y])


def resource_value(landscape):
	wooded_acres = 0
	lumberyards = 0

	for y in range(lumber_area_size):
		for x in range(lumber_area_size):
			if landscape[y][x] == wooded:
				wooded_acres += 1
			elif landscape[y][x] == lumberyard:
				lumberyards += 1

	return wooded_acres * lumberyards


def valid_coordinate(x, y):
	return x >= 0 and x < lumber_area_size and y >= 0 and y < lumber_area_size


def change_acre(X, Y, landscape):
	adjacent_wooded = 0
	adjacent_open_grounds = 0
	adjacent_lumberyards = 0

	for i in range(8):
		x = X + col_num[i]
		y = Y + row_num[i]

		if valid_coordinate(x, y):
			if landscape[y][x] == wooded:
				adjacent_wooded += 1

			elif landscape[y][x] == open_ground:
				adjacent_open_grounds += 1

			else:
				adjacent_lumberyards += 1

	current_acre = landscape[Y][X]
	future_acre = current_acre

	if current_acre == open_ground and adjacent_wooded > 2:
		future_acre = wooded
	elif current_acre == wooded and adjacent_lumberyards > 2:
		future_acre = lumberyard
	elif current_acre == lumberyard:
		if adjacent_wooded and adjacent_lumberyards:
			future_acre = lumberyard
		else:
			future_acre = open_ground

	return future_acre


landscape_dict = dict()
landscape_hash_list = list()
repetition_interval = 0
repetition_start_minute = 0
first_result = 0

for minute in range(1, SECOND_RESULT_MINUTE + 1):
	changed_landscape = deepcopy(landscape)

	for y in range(lumber_area_size):
		for x in range(lumber_area_size):
			changed_landscape[y][x] = change_acre(x, y, landscape)

	landscape = changed_landscape

	print_map(minute, landscape)

	h = hashlib.sha256()
	flattened_landscape = "".join(flatten_landscape(landscape))
	h.update(bytes(flattened_landscape.encode("utf8")))
	landscape_hash = h.hexdigest()

	if landscape_hash not in landscape_dict:
		landscape_dict[landscape_hash] = [minute, resource_value(landscape)]
		landscape_hash_list.append(landscape_hash)

		if minute == FIRST_RESULT_MINUTE:
			first_result = landscape_hash

	else:
		#first repetition, stop
		repetition_interval = minute - landscape_dict[landscape_hash][0]
		repetition_start_minute = minute
		break


print("Resource value after %u minutes is %u" % (FIRST_RESULT_MINUTE, landscape_dict[first_result][1]))
total_resource = landscape_dict[landscape_hash_list[-repetition_interval + ((SECOND_RESULT_MINUTE - minute) % repetition_interval)]][1]
print("Resource value after %u minutes is %u" % (SECOND_RESULT_MINUTE, total_resource))
