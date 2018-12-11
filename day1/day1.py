import os

base_file = os.path.splitext(__file__)[0]

frequency_changes = []

with open(base_file + ".input", "r") as fo:
    for line in fo:
        frequency_changes.append(int(line))

print("Resulting frequency", sum(frequency_changes))

duplicate_frequency_found = False
iteration = 0
running_frequency = 0
frequencies = [running_frequency, ]

while not duplicate_frequency_found:
     iteration = iteration + 1
     print(".", end='', flush=True)
     for frequency_change in frequency_changes:
            running_frequency = running_frequency + frequency_change
            if running_frequency not in frequencies:
                frequencies.append(running_frequency)
            else:
                duplicate_frequency_found = True
                print("")
                break

print("First frequency reached twice is", running_frequency)
