import os
import sys

base_file = os.path.splitext(__file__)[0]

box_ids = []

with open(base_file + ".input", "r") as fo:
    for line in fo:
        box_ids.append(line.rstrip())

def count_char_occurrences(string):
	counts = dict()
	for c in string:
		if c in counts:
			counts[c] = counts[c] + 1
		else:
			counts[c] = 1
	return counts

twos = 0
threes = 0

for box_id in box_ids:
	occurrences = count_char_occurrences(box_id)
	different_char_counts = set(occurrences.values())
	if 2 in different_char_counts:
		twos = twos + 1
	if 3 in different_char_counts:
		threes = threes + 1

print("Checksum is", twos * threes)

for i in range(len(box_ids) - 1):
	for j in range(i, len(box_ids)):
		diff = 0
		result = ""
		for k in range(len(box_ids[i])):
			if (box_ids[i][k] != box_ids[j][k]):
				diff = diff + 1
			else:
				result += box_ids[i][k]
		if diff == 1:
			print("Common letters are", result)
			sys.exit()




