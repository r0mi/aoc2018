# Let the 6 register be called A B ip C D E

#  0 seti 123 0 3         # C = 123
#  1 bani 3 456 3         # C &= 456      | C = 72
#  2 eqri 3 72 3          # C = (C == 72) | C = 1
#  3 addr 3 2 2           # ip += C       | ip = 4 | GOTO 5
#  4 seti 0 0 2           # ip = 0        | GOTO 1

#  5 seti 0 6 3           # C = 0
#  6 bori 3 65536 4       # D = C | 65536 | D = 65536
#  7 seti 2176960 8 3     # C = 2176960
#  8 bani 4 255 1         # B = D & 255   | B = 0
#  9 addr 3 1 3           # C += B        | C = 2176960
# 10 bani 3 16777215 3    # C &= 16777215 | C = 2176960
# 11 muli 3 65899 3       # C *= 65899    | C = 143459487040
# 12 bani 3 16777215 3    # C &= 16777215 | C = 14290240

# if (256 > D)
# 	GOTO 28
# else
# 	GOTO 17
# 13 gtir 256 4 1         # B = (256 > D) | B = 0
# 14 addr 1 2 2           # ip += B       | ip = 14/15 | GOTO 15/16
# 15 addi 2 1 2           # ip += 1       | ip = 16 | GOTO 17
# 16 seti 27 7 2          # ip = 27       | GOTO 28

# 17 seti 0 9 1           # B = 0
# 18 addi 1 1 5           # E = B + 1
# 19 muli 5 256 5         # E *= 256

# if (E > D)
# 	GOTO 26
# else
# 	B = 1
# 	GOTO 18
# 20 gtrr 5 4 5           # E = (E > D)   | E = 0
# 21 addr 5 2 2           # ip += E       | ip = 21/22 | GOTO 22/23
# 22 addi 2 1 2           # ip += 1       | ip = 23 | GOTO 24
# 23 seti 25 7 2          # ip = 25       | GOTO 26
# 24 addi 1 1 1           # B += 1        | B = 1
# 25 seti 17 2 2          # ip = 17       | GOTO 18

# 26 setr 1 7 4           # D = B         | D = 2
# 27 seti 7 9 2           # ip = 7        | GOTO 8

# if (C == A)
# 	RETURN
# else
# 	GOTO 6
# 28 eqrr 3 0 1           # B = (C == A)  | B = 0
# 29 addr 1 2 2           # ip += B       | ip = 29/30 | GOTO 30 / RETURN
# 30 seti 5 9 2           # ip = 5        | GOTO 6

# The main loop in short

A = B = C = D = E = 0
unique_c_values = set()
previous_unique_c = 0

while True:
	# 6:
	D = C | 65536
	C = 2176960

	while True:
		# 8:
		B = D & 255
		C += B
		C &= 16777215
		C *= 65899
		C &= 16777215

		if 256 > D:
			if len(unique_c_values) == 0:
				print("Lowest register 0 value that causes the program to execute fewest instructions is", C)

			if C not in unique_c_values:
				previous_unique_c = C
				unique_c_values.add(C)

			else: # C values start to repeat, exit with previous unique value
				print("Lowest register 0 value that causes the program to execute most instructions is", previous_unique_c)
				exit(1)

			if C == A:
				exit(1)
			else:
				# GOTO 6
				break
		else:
			# GOTO 17
			# Optimised the following loop to
			D >>= 8 # Basically dividing by 256 in a very slow manner
			# 17:
			# B = 0
			# while True:
			# 	# 18:
			# 	E = (B + 1) * 256

			# 	if E > D:
			# 		D = B
			# 		# GOTO 8
			# 		break
			# 	else:
			# 		B += 1
			# 		# GOTO 18
