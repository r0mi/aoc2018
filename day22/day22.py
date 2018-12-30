import os
import sys
import time
import random
from queue import PriorityQueue
from collections import defaultdict

base_file = os.path.splitext(__file__)[0]

DEPTH = 5913
TARGET = (8, 701)
MOUTH = (0, 0)

types = {
	0 : ".", # Rock (T,C)
	1 : "=", # Wet (C,N)
	2 : "|", # Narrow (T,N)
}

gear = {
	0: 'Torch',
	1: 'Climbing',
	2: 'Neither',
}

cave_system = defaultdict(dict)

def get_region_specs(x, y):
	global cave_system

	specs = {}

	if cave_system[(x, y)] != {}:
		return cave_system[(x, y)]

	if (x, y) in [MOUTH, TARGET]:
		geological_index = 0

	elif x == 0:
		geological_index = y * 48271

	elif y == 0:
		geological_index = x * 16807

	else:
		if cave_system[(x - 1, y)] == {}:
			cave_system[(x - 1, y)] = get_region_specs(x - 1, y)

		if cave_system[(x, y - 1)] == {}:
			cave_system[(x, y - 1)] = get_region_specs(x, y - 1)

		geological_index = cave_system[(x - 1, y)]['erosion_level'] * cave_system[(x, y - 1)]['erosion_level']

	erosion_level = (geological_index + DEPTH) % 20183
	specs['geological_index'] = geological_index
	specs['erosion_level'] = erosion_level
	specs['type'] = erosion_level % 3
	cave_system[(x, y)] = specs

	return specs

risk = 0
fo = open(base_file + "_initial_map.output", "w")
for y in range(TARGET[1] + 1):
	for x in range(TARGET[0] + 1):
		specs = get_region_specs(x, y)
		risk += specs['type']

		if (x, y) == MOUTH:
			fo.write('M')

		elif (x, y) == TARGET:
			fo.write('T')

		else:
			fo.write(types[specs['type']])

	fo.write('\n')

fo.close()


print("The area risk level is", risk)

row_num = [-1, 0, 1,  0]
col_num = [ 0, 1, 0, -1]

def heuristic_cost_estimate(a, b):
	(x1, y1) = a
	(x2, y2) = b
	return abs(x1 - x2) + abs(y1 - y2)

def choose_prev(tool):
	return (tool - 1) % 3

def cost_fn(a, b, goal, tool_choose_fn):
	((x1, y1), t1) = a
	((x2, y2), t2) = b

	if x2 < 0 or x2 >= 100 or y2 < 0 or y2 >= 1000:
		return (sys.maxsize, t1)

	if (x2, y2) == goal:
		if t1 == 0:
			return (1, 0)
		else:
			return (8, 0)

	if get_region_specs(x1, y1)['type'] == get_region_specs(x2, y2)['type']:
		return (1, t1)

	elif get_region_specs(x2, y2)['type'] == 0 and t1 in [0, 1] or get_region_specs(x2, y2)['type'] == 1 and t1 in [1, 2] or get_region_specs(x2, y2)['type'] == 2 and t1 in [0, 2]:
		return (1, t1)

	else:
		return (8, tool_choose_fn(t1))


def reconstruct_path(came_from, current):
    total_path = [current]

    while current in came_from.keys():
        current = came_from[current]
        total_path.append(current)

    return total_path


def a_star_search(start, goal, start_tool, goal_tool, cost_fn):
	# closed_set = {}
	open_set = PriorityQueue()
	open_set.put((0, (start, start_tool)), block=False)

	came_from = {}
	g_score = {}
	g_score[start] = 0

	tools = {}
	tools[start] = start_tool

	f_score = {}
	f_score[start] = heuristic_cost_estimate(start, goal)

	while not open_set.empty():
		# print(open_set.qsize())
		priority, (current, current_tool) = open_set.get(block=False)

		if current == goal:
			break

		# closed_set[current] = 1

		# For each neighbour of current
		for i in range(4):
			neighbour = (current[0] + col_num[i], current[1] + row_num[i])

			# if neighbour in closed_set:
			# 	continue

			if neighbour == goal:
				neighbour_tool = goal_tool
			else:
				neighbour_tool = current_tool

			# The distance from start to a neighbour
			neighbour_cost, neighbour_tool = cost_fn((current, current_tool), (neighbour, neighbour_tool), goal)
			tentative_g_score = g_score[current] + neighbour_cost

			if neighbour not in g_score or tentative_g_score < g_score[neighbour]:
				# This path is the best until now. Record it!
				came_from[neighbour] = current
				g_score[neighbour] = tentative_g_score
				f_score[neighbour] = g_score[neighbour] + heuristic_cost_estimate(neighbour, goal)
				tools[neighbour] = neighbour_tool

				open_set.put((f_score[neighbour], (neighbour, neighbour_tool)), block=False)

	return came_from, g_score, tools

came_from, cost_so_far, tools = a_star_search(MOUTH, TARGET, 0, 0, lambda a, b, c: cost_fn(a, b, c, choose_prev))
path = reconstruct_path(came_from, TARGET)
path.reverse()
print("Fewest number of minutes to reach the target is", cost_so_far[path[-1]])

route = {}
for x in path[1:]:
	route[x] = 1

fo = open(base_file + "_solution_map.output", "w")
for y in range(TARGET[1] + 100):
	for x in range(TARGET[0] + 100):
		specs = get_region_specs(x, y)

		if (x, y) == MOUTH:
			fo.write('M')

		elif (x, y) == TARGET:
			fo.write('T')

		elif (x, y) in route:
			fo.write('#')

		else:
			fo.write(types[specs['type']])

	fo.write('\n')

fo.close()
