import os
from queue import Queue

base_file = os.path.splitext(__file__)[0]

points = set()

with open(base_file + ".input", "r") as fo:
	for line in fo:
		points.add(tuple(map(int, line.rstrip().split(','))))

constellations = []

def manhattan_distance(p1, p2):
	x1, y1, z1, w1 = p1
	x2, y2, z2, w2 = p2
	return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2) + abs(w1 - w2)

processed = set()
queue = Queue()

while len(points):
	constellation = []

	queue.put(points.pop(), block=False)

	while not queue.empty():
		p1 = queue.get(block=False)

		constellation.append(p1)

		for p2 in points.copy():
			if manhattan_distance(p1, p2) <= 3:
				points.remove(p2)
				queue.put(p2, block=False)

		processed.add(p1)

	constellations.append(constellation)

points = processed.copy()

print("%u constellations are formed by the fixed points in spacetime" % len(constellations))