import os
import re
import time

base_file = os.path.splitext(__file__)[0]

regex = re.compile(r"position=<(?P<position>[0-9- ,]*)> velocity=<(?P<velocity>[0-9- ,]*)>")

points = []

with open(base_file + ".input", "r") as fo:
	for line in fo:
		match = regex.search(line.rstrip())
		if match:
			points.append((tuple(map(int, match.group("position").split(", "))),tuple(map(lambda x: int(x.strip()), match.group("velocity").split(", ")))))

previous_points = []
previous_canvas_dimensions = None
run = True
iteration = 0

while run:
	iteration = iteration + 1
	moved_points = []

	for point in points:
		x = point[0][0] + iteration * point[1][0]
		y = point[0][1] + iteration * point[1][1]
		moved_points.append([x, y])

	x_min = min(moved_points, key=lambda x: x[0])[0]
	x_max = max(moved_points, key=lambda x: x[0])[0]
	y_min = min(moved_points, key=lambda x: x[1])[1]
	y_max = max(moved_points, key=lambda x: x[1])[1]
	current_canvas_dimensions = abs(x_min - x_max) * abs(y_min - y_max)

	if previous_canvas_dimensions and previous_canvas_dimensions < current_canvas_dimensions:
		# Previous iteration had smaller canvas, probably containing the answer
		iteration = iteration - 1
		run = False
	else:
		previous_canvas_dimensions = current_canvas_dimensions
		previous_points = moved_points

previous_points.sort(key=lambda x: x[1])
x_min = min(previous_points, key=lambda x: x[0])[0]
x_max = max(previous_points, key=lambda x: x[0])[0]
y_min = min(previous_points, key=lambda x: x[1])[1]
y_max = max(previous_points, key=lambda x: x[1])[1]
answer_points = list(map(lambda pt: (pt[0] - x_min, pt[1] - y_min), previous_points))

for y in range(y_max - y_min + 1):
	for x in range(x_max - x_min + 1):
		if (x, y) in answer_points:
			print("#", end="")
		else:
			print(" ", end="")
	print("")

print()
print("Total seconds needed to wait", iteration)
