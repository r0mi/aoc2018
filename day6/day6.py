import os
import string

TOTAL_DISTANCE = 10000

base_file = os.path.splitext(__file__)[0]

coordinates = []

with open(base_file + ".input", "r") as fo:
	for line in fo:
		x, y, = line.rstrip().split(", ")
		coordinates.append((int(x), int(y)))

map_width = max(coordinates, key=lambda pt: pt[0])[0] + 1
map_height = max(coordinates, key=lambda pt: pt[1])[1] + 1

map_ = [["" for y in range(map_height)] for x in range(map_width)]

# Draw initial map
with open(base_file + "_map.output", "w") as fo:
	for x in range(map_width):
		for y in range(map_height):
			if (x, y) in coordinates:
				fo.write(string.printable[coordinates.index((x, y))])
			else:
				fo.write(".")
		fo.write("\n")

infite_areas = set()
areas = dict(zip(list(string.printable[:len(coordinates)]), [0] * len(coordinates)))
with open(base_file + "_location_area_map.output", "w") as fo:
	for x in range(map_width):
		for y in range(map_height):
			distances = dict()
			for i, (x_, y_) in enumerate(coordinates):
				distances[i] = abs(x - x_) + abs(y - y_)
			keys = sorted(distances, key=distances.get)
			if distances[keys[0]] != distances[keys[1]]:
				if (x, y) == coordinates[keys[0]]:
					fo.write(" ")
				else:
					fo.write(string.printable[keys[0]])
				map_[x][y] = string.printable[keys[0]]
				if x == 0 or x == map_width - 1 or y == 0 or y == map_height - 1:
					infite_areas.add(string.printable[keys[0]])
				areas[string.printable[keys[0]]] = areas[string.printable[keys[0]]] + 1
			else:
				fo.write(".")
				map_[x][y] = "."
		fo.write("\n")

# Filter out infinte areas
areas = dict(filter(lambda x: x[0] not in infite_areas, areas.items()))
largest_area_key = max(areas, key=areas.get)

print("Largest finite area is %u for location (%u, %u)" % (areas[largest_area_key], coordinates[string.printable.index(largest_area_key)][0], coordinates[string.printable.index(largest_area_key)][1]))

region_size = 0
with open(base_file + "_total_distance_map.output", "w") as fo:
	for x in range(map_width):
		for y in range(map_height):
			distances = list()
			distance = 0
			current_location_index = None
			for i, (x_, y_) in enumerate(coordinates):
				distance = distance + abs(x - x_) + abs(y - y_)
				if (x, y) == coordinates[i]:
					current_location_index = i
			if distance < TOTAL_DISTANCE:
				region_size = region_size + 1
				if current_location_index:
					fo.write(string.printable[current_location_index])
				else:
					fo.write("#")
			else:
				if current_location_index:
					fo.write(string.printable[current_location_index])
				else:
					fo.write(".")
		fo.write("\n")

print("Region size containing all coordinates with total distance below %u is %u" % (TOTAL_DISTANCE, region_size))