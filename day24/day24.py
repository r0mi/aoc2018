import os
import re
from copy import deepcopy
from math import floor

base_file = os.path.splitext(__file__)[0]

regex = re.compile(r"(?P<type>[\w ]+):|(?P<num_units>\d+).*?(?P<hit_points>\d+).*?(\((?P<properties>.*)\))? with.*?(?P<attack_damage>\d+) (?P<attak_type>\w+).*?(?P<initiative>\d+)|^.{0}$")
properties_regex = re.compile(r"immune to (?P<immunities>[\w ,]+);?|weak to (?P<weaknesses>[\w ,]+);?")

armies_by_type = {"Immune System": {}, "Infection": {}}

class Unit:
	def __init__(self, type, num, num_units, hit_points, attack_damage, attak_type, initiative, immunities, weaknesses):
		self.type = type
		self.num = num
		self.num_units = num_units
		self.hit_points = hit_points
		self.attack_damage = attack_damage
		self.attak_type = attak_type
		self.initiative = initiative
		self.immunities = immunities
		self.weaknesses = weaknesses
		self.attack_next = None

	def boost(self, amount):
		self.attack_damage += amount

	def effective_power(self):
		return self.num_units * self.attack_damage

	def attacks(self):
		return "Infection" if self.type == "Immune System" else "Immune System"

	def damage_dealt(self, unit):
		if unit.attak_type in self.immunities:
			return 0

		elif unit.attak_type in self.weaknesses:
			return unit.effective_power() * 2

		else:
			return unit.effective_power()

	def attack(self):
		if self.attack_next:
			kills = self.attack_next.defend(self)
			return kills

		else:
			return None

	def defend(self, unit):
		kills = min(self.damage_dealt(unit) // self.hit_points, self.num_units)
		self.num_units -= kills
		return kills

	def print(self):
		base = "%s group %u EP %u, I %u: %u units, %u hit_points, %u %s damage" % (
			self.type, self.num, self.effective_power(), self.initiative, self.num_units, self.hit_points,
			self. attack_damage, self.attak_type)

		properties = []

		if self.immunities:
			properties.append("immune to " + ", ".join(self.immunities))

		if self.weaknesses:
			properties.append("weak to " + ", ".join(self.weaknesses))

		if properties:
			base += " (" + "; ".join(properties) + ")"

		return base

	def __str__(self):
		return "%s group %u" % (self.type, self.num)


with open(base_file + ".input", "r") as fo:
	current_type = None
	count = 0

	for line in fo:
		match = regex.search(line.rstrip())

		if match:
			if match.group("type"):
				current_type = match.group("type")
				count = 0

			elif match.group("num_units"):
				count += 1
				immunities = []
				weaknesses = []

				if match.group("properties"):
					properties = match.group("properties").split("; ")

					for prop in properties:
						m = properties_regex.search(prop)

						if m:
							if m.group("immunities"):
								immunities = m.group("immunities").split(', ')

							elif m.group("weaknesses"):
								weaknesses = m.group("weaknesses").split(', ')

				unit = Unit(
					current_type,
					count,
					int(match.group("num_units")),
					int(match.group("hit_points")),
					int(match.group("attack_damage")),
					match.group("attak_type"),
					int(match.group("initiative")),
					immunities,
					weaknesses
				)

				armies_by_type[unit.type][unit.num] = unit


def copy_armies(armies_by_type):
	by_type_copy = deepcopy(armies_by_type)
	armies_copy = []

	for type, armies in by_type_copy.items():
		for key, unit in armies.items():
			armies_copy.append(unit)

	return by_type_copy, armies_copy


def simulate(armies_by_type, all_armies, boost_attack):
	if boost_attack:
		for key, unit in armies_by_type['Immune System'].items():
			unit.boost(boost_attack)

	dead_end = False

	while not dead_end and len(armies_by_type['Immune System']) and len(armies_by_type['Infection']):
		all_armies.sort(key=lambda unit: (unit.effective_power(), unit.initiative), reverse=True)

		total_units_before = 0

		for unit in all_armies:
			total_units_before += unit.num_units

		# print()

		# for typ, units in armies_by_type.items():
		# 	print(typ)

		# 	for key, unit in units.items():
		# 		print("Group %u contains %u units" % (key, unit.num_units))

		# print()

		# Target selection
		units_chosen = {"Immune System": set(), "Infection": set()}

		for unit in all_armies:
			choices = []

			for num, enemy_unit in armies_by_type[unit.attacks()].items():
				if num not in units_chosen[unit.attacks()]:
					damage = enemy_unit.damage_dealt(unit)

					if damage:
						choices.append((damage, enemy_unit.effective_power(), enemy_unit.initiative, enemy_unit))
						# print("%s group %u would deal defending group %u %u damage (EP %u, I %u)" % (unit.type, unit.num, num, damage, enemy_unit.effective_power(), enemy_unit.initiative))

			if choices:
				choices.sort(reverse=True)
				chosen = choices[0][3]
				units_chosen[unit.attacks()].add(chosen.num)
				unit.attack_next = chosen

			else:
				unit.attack_next = None

		# print()

		all_armies.sort(key=lambda unit: unit.initiative, reverse=True)

		# Attacking
		for unit in all_armies:
			if unit.attack_next and unit.num_units:
				num = unit.attack_next.num
				kills = unit.attack()
				# print(unit, "attacks defending group %u, killing %u units" % (num, kills))

		# print()
		for i, unit in enumerate(all_armies):
			if unit.num_units == 0:
				del armies_by_type[unit.type][unit.num]
				all_armies.pop(i)


		total_units_after = 0
		for unit in all_armies:
			total_units_after += unit.num_units

		if total_units_before == total_units_after:
			dead_end = True

	if dead_end:
		return (None, 0)

	result = 0
	winning_army = None

	for typ, units in armies_by_type.items():
		if len(units):
			winning_army = typ

		for key, unit in units.items():
			result += unit.num_units

	return (winning_army, result)

by_type_armies, all_armies = copy_armies(armies_by_type)
won, result = simulate(by_type_armies, all_armies, 0)
print("The winning army (%s) would have %u units" % (won, result))

test_boost = 1

while True:
	by_type_armies, all_armies = copy_armies(armies_by_type)

	winning_army, units = simulate(by_type_armies, all_armies, test_boost)

	if winning_army == "Infection" or winning_army == None:
		test_boost += 1

	else:
		print("With boost %u the immune system barely wins with %u units left" % (test_boost, units))
		break
