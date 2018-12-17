import os
import re

base_file = os.path.splitext(__file__)[0]

regex = re.compile(r"After:\s+\[(?P<after>[\d, ]*)\]|Before:\s+\[(?P<before>[\d, ]*)\]|(?P<instruction>[\d ]*)|^.{0}$")

io_samples = []
test_program = []

with open(base_file + ".input", "r") as fo:
	sample = {}

	empty = 0
	for line in fo:
		match = regex.search(line.rstrip())

		if match:
			if match.group("before"):
				sample = {'before': list(map(int, match.group("before").split(", ")))}
				empty = 0

			elif match.group("instruction"):
				if empty < 3:
					sample['instruction'] = list(map(int, match.group("instruction").split(" ")))

				else:
					test_program.append(list(map(int, match.group("instruction").split(" "))))

			elif match.group("after"):
				sample['after'] = list(map(int, match.group("after").split(", ")))
				io_samples.append(sample)

			else:
				empty += 1

# Define functions:
def addr(a, b, c):
	REGISTERS[c] = REGISTERS[a] + REGISTERS[b]

def addi(a, b, c):
	REGISTERS[c] = REGISTERS[a] + b

def mulr(a, b, c):
	REGISTERS[c] = REGISTERS[a] * REGISTERS[b]

def muli(a, b, c):
	REGISTERS[c] = REGISTERS[a] * b

def banr(a, b, c):
	REGISTERS[c] = REGISTERS[a] & REGISTERS[b]

def bani(a, b, c):
	REGISTERS[c] = REGISTERS[a] & b

def borr(a, b, c):
	REGISTERS[c] = REGISTERS[a] | REGISTERS[b]

def bori(a, b, c):
	REGISTERS[c] = REGISTERS[a] | b

def setr(a, b, c):
	REGISTERS[c] = REGISTERS[a]

def seti(a, b, c):
	REGISTERS[c] = a

def gtir(a, b, c):
	REGISTERS[c] = 1 if a > REGISTERS[b] else 0

def gtri(a, b, c):
	REGISTERS[c] = 1 if REGISTERS[a] > b else 0

def gtrr(a, b, c):
	REGISTERS[c] = 1 if REGISTERS[a] > REGISTERS[b] else 0

def eqir(a, b, c):
	REGISTERS[c] = 1 if a == REGISTERS[b] else 0

def eqri(a, b, c):
	REGISTERS[c] = 1 if REGISTERS[a] == b else 0

def eqrr(a, b, c):
	REGISTERS[c] = 1 if REGISTERS[a] == REGISTERS[b] else 0

functions = {
	'addr' : addr,
	'addi' : addi,
	'mulr' : mulr,
	'muli' : muli,
	'banr' : banr,
	'bani' : bani,
	'borr' : borr,
	'bori' : bori,
	'setr' : setr,
	'seti' : seti,
	'gtir' : gtir,
	'gtri' : gtri,
	'gtrr' : gtrr,
	'eqir' : eqir,
	'eqri' : eqri,
	'eqrr' : eqrr,
}

similar_behaviour = 0

opcodes = dict(zip(list(range(len(functions))), [set() for x in range(len(functions))]))

REGISTERS = []

for sample in io_samples:
	similar_count = 0

	for name, fun in functions.items():
		REGISTERS = sample['before'][:]
		fun(*sample['instruction'][1:])

		if REGISTERS == sample['after']:
			opcodes[sample['instruction'][0]].add(name)
			similar_count += 1

	if similar_count >= 3:
		similar_behaviour += 1

print("%d samples behave like three or more opcodes" % similar_behaviour)

for x in range(len(opcodes)):
	for opcode_number, possible_opcodes in opcodes.copy().items():
		if type(possible_opcodes) == set and len(possible_opcodes) == 1:
			fun = list(possible_opcodes)[0]
			opcodes[opcode_number] = functions[fun]
			print("Opcode %2u corresponds to function %s" % (opcode_number, fun))

			for k, v in opcodes.items():
				if type(v) == set and fun in v:
					v.remove(fun)

REGISTERS = [0, 0, 0, 0]

for operation in test_program:
	opcodes[operation[0]](*operation[1:])

print("%d is contained in register 0 after executing the test program" % REGISTERS[0])



