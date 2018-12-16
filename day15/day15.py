import os
import sys
import time
from copy import copy, deepcopy
from functools import reduce
import random

HEALTH_POINTS = 200
ATTACK_POWER = 3

base_file = os.path.splitext(__file__)[0]

cave_map = []
creatures = []
creature_types = "GE"
creature_locations = dict()

class Cell:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		return "(%u,%u)" % (self.x, self.y)


class Creature:
	def __init__(self, type_, cell, hp):
		self.type = type_
		self.location = cell
		self.hp = hp
		self.enemy = creature_types.strip(type_)

	def attack(self, target):
		target.hp -= ATTACK_POWER
		return target.hp > 0

	def dead(self):
		return self.hp <= 0

	def __str__(self):
		return self.type + "(%u, (%u,%u))" % (self.hp, self.location.x, self.location.y)


class Node:
	def __init__(self, cell, distance):
		self.cell = cell
		self.distance = distance

	def __str__(self):
		return "(%u,%u)=%u" % (self.cell.x, self.cell.y, self.distance)


with open(base_file + ".input", "r") as fo:
	for y, line in enumerate(fo):
		row = []
		for x, cell in enumerate(line.rstrip()):
			row.append(cell);
			if cell in creature_types:
				creature = Creature(cell, Cell(x, y), HEALTH_POINTS)
				creatures.append(creature)
				creature_locations[(x,y)] = creature
		cave_map.append(row)

map_width = len(cave_map[0])
map_height = len(cave_map)

row_num = [-1, 0, 0, 1]
col_num = [0, -1, 1, 0]

def sort_creatures(creatures):
	creatures.sort(key=lambda creature: (creature.location.y, creature.location.x))


def print_map(round_):
	os.system("clear")
	print("Round #", round_, "creatures", len(creatures), len(creature_locations))
	for y, row in enumerate(cave_map):
		cs = []
		for x, cell in enumerate(row):
			print(cell, end='')
			if (x,y) in creature_locations:
				cs.append(creature_locations[(x,y)])
		print("   " + ", ".join(list(map(str, cs))))

def print_map_with_overlay(overlay_items, overlay_char='*'):
	for y, row in enumerate(cave_map):
		for x, cell in enumerate(row):
			if (x,y) in overlay_items:
				print(overlay_char, end='')
			else:
				print(cell, end='')
		print()

def find_targets(enemy, creatures):
	return list(filter(lambda creature: creature.type == enemy and creature.hp > 0, creatures))

def is_valid(col, row):
	return col >= 0 and col < map_width and row >= 0 and row < map_height

def enemy_in_range(attacker):
	weakest = []

	for i in range(4):
		row = attacker.location.y + row_num[i]
		col = attacker.location.x + col_num[i]

		if (col, row) in creature_locations and creature_locations[(col, row)].type == attacker.enemy and creature_locations[(col, row)].hp > 0:
			weakest.append(creature_locations[(col, row)])

	if weakest:
		return sorted(weakest, key=lambda c: (c.hp, c.location.y, c.location.x))[0]

	return None


def in_range_spots(targets):
	in_range = set()

	for target in targets:
		loc = target.location

		if cave_map[loc.y][loc.x - 1] == '.':
			in_range.add(Cell(loc.x - 1, loc.y))
		if cave_map[loc.y][loc.x + 1] == '.':
			in_range.add(Cell(loc.x + 1, loc.y))
		if cave_map[loc.y - 1][loc.x] == '.':
			in_range.add(Cell(loc.x, loc.y - 1))
		if cave_map[loc.y + 1][loc.x] == '.':
			in_range.add(Cell(loc.x, loc.y + 1))

	return in_range


def calc_distance_map(start):
	distance_map = [[-1 for x in range(map_width)] for y in range(map_height)]
	distance_map[start.y][start.x] = 0
	next_distance = 0
	queue = [start]

	while len(queue):
		locations = queue
		queue = []
		next_distance += 1

		for loc in locations:
			for i in range(4):
				row = loc.y + row_num[i]
				col = loc.x + col_num[i]

				if is_valid(col, row) and cave_map[row][col] == '.' and (distance_map[row][col] == -1):
					cell = Cell(col, row)
					queue.append(cell)
					distance_map[row][col] = next_distance

	# first = True
	# print("   ", end="")
	# for i in range(len(distance_map[0])):
	# 	print("%3d" % i, end="")
	# print()
	# for y, row in enumerate(distance_map):
	# 	for x, cell in enumerate(row):
	# 		if x == 0:
	# 			print("%3d" % y, end="")
	# 		if cell == -1:
	# 			print(" . ", end='')
	# 		else:
	# 			print("%3d" % cell, end='')
	# 	print()
	return distance_map

def find_next_step(start, end):
	distance_map = calc_distance_map(start)

	best = map_width * map_height
	step = None

	for i in range(4):
		row = end.y + row_num[i]
		col = end.x + col_num[i]

		if distance_map[row][col] > -1 and distance_map[row][col] < best:
			best = distance_map[row][col]
			step = Cell(col, row)

	return step

def bury_creature(creature):
	cave_map[creature.location.y][creature.location.x] = "."
	creature_locations.pop((creature.location.x, creature.location.y), None)
	creatures.remove(creature)


def attack(creature):
	enemy = enemy_in_range(creature)

	if enemy != None:
		if not creature.attack(enemy):
			bury_creature(enemy)

		return True

	return False



def move(creature, targets):
	in_range = in_range_spots(targets)
	distance_map = calc_distance_map(creature.location)
	closest = []
	shortest = None

	for p in in_range:
		if distance_map[p.y][p.x] > 0 and (shortest == None or distance_map[p.y][p.x] < shortest):
			shortest = distance_map[p.y][p.x]
			closest = [p]
		elif distance_map[p.y][p.x] == shortest:
			closest.append(p)

	if shortest:
		nearest = sorted(closest, key=lambda c: (c.y, c.x))[0]
	else:
		nearest = None

	if nearest:
		return find_next_step(nearest, creature.location)

	return None



def proceed_round(round_nr):
	creature = None

	for i, cr in enumerate(deepcopy(creatures)):
		if (cr.location.x, cr.location.y) not in creature_locations:
			# Creature has died
			continue
		else:
			creature = creature_locations[(cr.location.x, cr.location.y)]

		loc = copy(creature.location)

		if attack(creature):
			continue

		targets = find_targets(creature.enemy, creatures)

		if i == 0 and not targets:
			return False

		step = move(creature, targets)

		if step != None:
			cave_map[loc.y][loc.x] = "."
			cave_map[step.y][step.x] = creature.type
			creature.location.x = step.x
			creature.location.y = step.y
			c = creature_locations.pop((loc.x, loc.y), None)
			creature_locations[(step.x, step.y)] = c

			attack(creature)

	return True


def combat():
	iteration = 0
	print_map(iteration)

	while proceed_round(iteration):
		iteration += 1
		print_map(iteration)
		sort_creatures(creatures)

	print_map(iteration - 1)
	print("Total score after %d iterations" % (iteration - 1), (iteration - 1) * sum(map(lambda c: c.hp, creatures)))
	return

combat()
