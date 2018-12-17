import os
import time
from copy import copy, deepcopy
from math import floor

HEALTH_POINTS = 200
ATTACK_POWER = 3

base_file = os.path.splitext(__file__)[0]

cave_map = []
creatures = []
creature_types = "GE"
creature_locations = dict()

row_num = [-1, 0, 0, 1]
col_num = [0, -1, 1, 0]

MAP_WIDTH = 0
MAP_HEIGHT = 0

class Cell:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		return "(%u,%u)" % (self.x, self.y)


class Creature:
	def __init__(self, type_, cell, hp, attack_power):
		self.type = type_
		self.location = cell
		self.hp = hp
		self.enemy = creature_types.strip(type_)
		self.attack_power = attack_power

	def attack(self, target):
		target.hp -= self.attack_power
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


def load_initial_data(cave_map, creatures, creature_locations, attack_power):
	cave_map.clear()
	creatures.clear()
	creature_locations.clear()

	with open(base_file + ".input", "r") as fo:
		for y, line in enumerate(fo):
			row = []

			for x, cell in enumerate(line.rstrip()):
				row.append(cell);

				if cell in creature_types:
					if cell == "E":
						creature = Creature(cell, Cell(x, y), HEALTH_POINTS, attack_power)

					else:
						creature = Creature(cell, Cell(x, y), HEALTH_POINTS, ATTACK_POWER)

					creatures.append(creature)
					creature_locations[(x,y)] = creature

			cave_map.append(row)

	return (len(cave_map[0]), len(cave_map))


def sort_creatures(creatures):
	creatures.sort(key=lambda creature: (creature.location.y, creature.location.x))


def print_map(round_):
	os.system("clear")
	print("Round #", round_, "elves", len(list(filter(lambda c: c.type == "E", creatures))), " Goblins", len(list(filter(lambda c: c.type == "G", creatures))))

	for y, row in enumerate(cave_map):
		cs = []

		for x, cell in enumerate(row):
			print(cell, end='')

			if (x,y) in creature_locations:
				cs.append(creature_locations[(x,y)])

		print("   " + ", ".join(list(map(str, cs))))


def find_targets(enemy, creatures):
	return list(filter(lambda creature: creature.type == enemy and creature.hp > 0, creatures))


def is_valid(col, row):
	return col >= 0 and col < MAP_WIDTH and row >= 0 and row < MAP_HEIGHT


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
	distance_map = [[-1 for x in range(MAP_WIDTH)] for y in range(MAP_HEIGHT)]
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

	return distance_map


def find_next_step(start, end):
	distance_map = calc_distance_map(start)

	best = MAP_WIDTH * MAP_HEIGHT
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


def combat(cave_map, creatures, creature_locations):
	iteration = 0
	print_map(iteration)

	elves = len(list(filter(lambda c: c.type == "E", creatures)))

	while proceed_round(iteration):
		iteration += 1
		print_map(iteration)
		sort_creatures(creatures)

	print_map(iteration - 1)
	score = (iteration - 1) * sum(map(lambda c: c.hp, creatures))

	return (score, iteration - 1, elves - len(list(filter(lambda c: c.type == "E", creatures))))


MAP_WIDTH, MAP_HEIGHT = load_initial_data(cave_map, creatures, creature_locations, ATTACK_POWER)

initial_score, iterations, elves_died = combat(cave_map, creatures, creature_locations)

minimum_attack_power = ATTACK_POWER
maximum_attack_power = minimum_attack_power * 2
test_attack_power = maximum_attack_power
tested_attack_power = {ATTACK_POWER: initial_score}
upper_bound_found = False

while True:
	load_initial_data(cave_map, creatures, creature_locations, test_attack_power)

	score, iterations, elves_died = combat(cave_map, creatures, creature_locations)
	print("With attack power %d %d elves die, total score after %d iterations %d" % (test_attack_power, elves_died, iterations, score))

	tested_attack_power[test_attack_power] = score

	if elves_died:
		if not upper_bound_found:
			minimum_attack_power = test_attack_power
			maximum_attack_power = minimum_attack_power * 2
			test_attack_power = maximum_attack_power

		else:
			minimum_attack_power = test_attack_power
			test_attack_power = int(floor((maximum_attack_power + minimum_attack_power) / 2. + 0.5))

	elif elves_died == 0:
		upper_bound_found = True
		maximum_attack_power = test_attack_power
		test_attack_power = (floor((maximum_attack_power + minimum_attack_power) / 2. + 0.5))

	if test_attack_power in tested_attack_power:
		os.system("clear")
		print("Initial score with attack power of %d is %d" % (ATTACK_POWER, tested_attack_power[ATTACK_POWER]))
		print("With attack power of %d, elves barely win with score %d" % (test_attack_power, tested_attack_power[test_attack_power]))
		break