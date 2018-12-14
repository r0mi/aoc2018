import os
import time
s = time.time()

base_file = os.path.splitext(__file__)[0]

frequency_changes = []

with open(base_file + ".input", "r") as fo:
    for line in fo:
        frequency_changes.append(int(line))

print("Resulting frequency", sum(frequency_changes))

duplicate_frequency_found = False
running_frequency = 0
frequency_dict = {0: 0}

while not duplicate_frequency_found:
    for f in frequency_changes:
        running_frequency += f
        if running_frequency in frequency_dict:
            duplicate_frequency_found = True
            break
        else:
            frequency_dict[running_frequency] = 0

print("First frequency reached twice is", running_frequency)
