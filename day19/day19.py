import os
import re

base_file = os.path.splitext(__file__)[0]

regex = re.compile(r"#ip (?P<ip>\d)|(?P<instruction>\w+) ((?P<operands>[\d ]+))")

IP = 0
IP_REGISTER = 0
REGISTERS = [0 for x in range(6)]
instructions = []

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

with open(base_file + ".input", "r") as fo:
	for line in fo:
		match = regex.search(line.rstrip())

		if match:
			if match.group("ip"):
				IP_REGISTER = int(match.group("ip"))

			elif match.group("instruction"):
				instructions.append([match.group("instruction"), list(map(int, match.group("operands").split(" ")))])

numbers_to_factor = []

REGISTERS[0] = 1

while 0 <= IP < len(instructions):
	REGISTERS[IP_REGISTER] = IP

	functions[instructions[IP][0]](*instructions[IP][1])
	# Find the factors for both parts and break

	if IP == 24:
		numbers_to_factor.append(REGISTERS[instructions[IP][1][2]])
	elif IP == 33:
		numbers_to_factor.append(REGISTERS[instructions[IP][1][2]])
		break

	IP = REGISTERS[IP_REGISTER] + 1


# As the program takes too long to finish analyze the instructions
# Let the 6 register be called A B C ip D E

#  0 addi 3 16 3# ip = 16 | GOTO 17
#  1 seti 1 8 1 # B = 1
#  2 seti 1 3 4 # D = 1

#  # if (B * D == E)
#  # 	GOTO 7
#  # else
#  # 	GOTO 8
#  3 mulr 1 4 2 # C = B * D
#  4 eqrr 2 5 2 # C = (C == E)
#  5 addr 2 3 3 # ip += C
#  6 addi 3 1 3 # ip += 1

#  7 addr 1 0 0 # A += B
#  8 addi 4 1 4 # D += 1

#  # if (D > E)
#  # 	GOTO 12
#  # else
#  #	GOTO 3
#  9 gtrr 4 5 2 # C = D > E
# 10 addr 3 2 3 # ip += C
# 11 seti 2 6 3 # ip = 2

# 12 addi 1 1 1 # B += 1

#  # if (B > E)
#  # 	GOTO 256 / RETURN
#  # else
#  # 	GOTO 2
# 13 gtrr 1 5 2 # C = (B > E)
# 14 addr 2 3 3 # ip += C
# 15 seti 1 5 3 # ip = 1
# 16 mulr 3 3 3 # ip *= ip

# 17 addi 5 2 5 # E += 2     | E = 2
# 18 mulr 5 5 5 # E *= E     | E = 4
# 19 mulr 3 5 5 # E *= ip/19 | E = 76
# 20 muli 5 11 5# E *= 11    | E = 836
# 21 addi 2 5 2 # C += 5     | C = 5
# 22 mulr 2 3 2 # C *= ip/22 | C = 110
# 23 addi 2 21 2# C += 21    | C = 131
# 24 addr 5 2 5 # E += C     | E = 967

# # PART 1: GOTO 1
# # PART 2: GOTO 27
# 25 addr 3 0 3 # ip += A
# 26 seti 0 4 3 # ip = A

# # PART 2
# 27 setr 3 1 2 # C  = ip/27 | C = 27
# 28 mulr 2 3 2 # C *= ip/28 | C = 756
# 29 addr 3 2 2 # C += ip/29 | C = 785
# 30 mulr 3 2 2 # C *= ip/30 | C = 23550
# 31 muli 2 14 2# C *= 14    | C = 329700
# 32 mulr 2 3 2 # C *= ip/32 | C = 10550400
# 33 addr 5 2 5 # E += C     | E = 10551367
# 34 seti 0 3 0 # A  = 0     | A = 0
# 35 seti 0 6 3 # ip = 0     | GOTO 1

# The main loop in short

# while True:
# 	if B * D == E:
# 		A += B
# 	D += 1
# 	if D > E:
# 		B += 1
# 		if B > E:
# 			break
# 		else:
# 			D = 1

# Seems to be finding the sum of factors of register E value

for j, n in enumerate(numbers_to_factor):
	init_n = n
	num_factors = 1
	i = 2
	factors = [1, n]

	while i * i < init_n:
		power = 0

		while n % i == 0:
			factors.append(i)
			n //= i

		i += 1

	if n > 1 and n != init_n:
		factors.append(n)

	print("Register 0 value when the program first halts the %u. time is %u" % (j + 1, sum(factors)))
