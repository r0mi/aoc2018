import os
import re
import time
import string

WORKERS = 5
STEP_TIME = 60

base_file = os.path.splitext(__file__)[0]

regex = re.compile(r"Step (?P<before>[A-Z]).*(?P<after>[A-Z]).*")

instructions = []
instruction_set = set()
instruction_before_set = set()
instruction_after_set = set()

with open(base_file + ".input", "r") as fo:
	for line in fo:
		match = regex.search(line.rstrip())
		if match:
			before = match.group("before")
			after = match.group("after")
			instruction_set.add(before)
			instruction_before_set.add(before)
			instruction_set.add(after)
			instruction_after_set.add(after)
			instructions.append((before, after))
		else:
			print("Bad instruction", line.rstrip())

instruction_map = dict()
instruction_map = dict(zip(sorted(instruction_set), [{'before': [], 'after': []} for x in range(len(instruction_set))]))
for before, after in instructions:
	instruction_map[before]['after'].append(after)
	instruction_map[before]['after'].sort()
	instruction_map[after]['before'].append(before)
	instruction_map[after]['before'].sort()

end_list = sorted(list(instruction_set - instruction_before_set))
start_list = sorted(list(instruction_set - instruction_after_set))

completed_instructions = list()
available_instructions = start_list.copy()

while available_instructions:
	current_instruction = None

	for instruction in available_instructions:
		if set(instruction_map[instruction]["before"]) - set(completed_instructions) == set():
			current_instruction = instruction
			break

	if current_instruction:
		available_instructions.remove(current_instruction)
		completed_instructions.append(current_instruction)

		if instruction_map[current_instruction]['after']:
			available_instructions = sorted(set(available_instructions + instruction_map[current_instruction]['after']))

print("Instruction set order", "".join(completed_instructions))

class Worker:
	def __init__(self, index):
		self.index = index
		self.operation = "."
		self.last_completed_operation = None
		self.time = 0

	def idle(self):
		return self.operation == "."

	def do(self, operation):
		self.operation = operation
		self.time = string.ascii_uppercase.index(operation) + 1 + STEP_TIME

	def tick(self):
		if self.time:
			self.time = self.time - 1

		operation = self.operation

		if operation != "." and not self.time:
			self.last_completed_operation = operation
			self.operation = "."

		return operation

	def finished(self):
		finished = self.last_completed_operation
		self.last_completed_operation = None
		return finished

	def __str__(self):
		return str(self.index)


duration = 0
workers = [Worker(i) for i in range(WORKERS)]
available_instructions = start_list
completed_instructions = list()

with open(base_file + ".output", "w") as fo:
	fo.write("Second   " + "".join(["Worker %s   " % w for w in workers]) + "Done\n")

	while len(completed_instructions) != len(instruction_set):
		# Get finished instructions
		for worker in workers:
			if worker.idle():
				completed_operation = worker.finished()
				if completed_operation:
					completed_instructions.append(completed_operation)
					if instruction_map[completed_operation]['after']:
						available_instructions = set(available_instructions + instruction_map[completed_operation]['after'])

		available_instructions = sorted(available_instructions)
		fo.write("% 4i     " % duration)

		# Process new instructions
		for worker in workers:
			if worker.idle():
				current_instruction = None

				for instruction in available_instructions:
					if set(instruction_map[instruction]["before"]) - set(completed_instructions) == set():
						current_instruction = instruction
						break

				if current_instruction:
					worker.do(instruction)
					available_instructions.remove(current_instruction)

			worker_task = worker.tick()
			fo.write("    %s       " % worker_task)

		fo.write("%s\n" % "".join(completed_instructions))

		if len(completed_instructions) != len(instruction_set):
			duration = duration + 1

print("Total time for completion", duration)
