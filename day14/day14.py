RECIPE_COUNT = 110201
SEQUENCE = list(reversed(list(map(int, str(RECIPE_COUNT)))))

recipes = [3, 7]
elf1_idx = 0
elf2_idx = 1

recipes_len = len(recipes)
seq_idx = 0

answer1_found = False
answer2_found = False

while not answer1_found or not answer2_found:
	elf1_recipe = recipes[elf1_idx]
	elf2_recipe = recipes[elf2_idx]

	append = []
	new_recipe = elf1_recipe + elf2_recipe

	if new_recipe > 9:
		append = [1, new_recipe - 10]
	else:
		append = [new_recipe, ]

	for recipe in append:
		recipes.append(recipe)
		recipes_len += 1

		if not answer2_found:
			for i in range(-1, -1 * len(SEQUENCE) - 1, -1):
				if recipes[i] == SEQUENCE[i * -1 - 1]:
					seq_idx += 1
				else:
					seq_idx = 0
					break
			if seq_idx == len(SEQUENCE):
				print("%d recipes appear on the scoreboard to the left of sequence %s" % (len(recipes) - len(SEQUENCE), str(RECIPE_COUNT)))
				answer2_found = True
				break

	if not answer1_found and recipes_len >= RECIPE_COUNT + 10:
		print("Ten recipes immediately after %d are %s" % (RECIPE_COUNT, "".join(map(str, recipes[RECIPE_COUNT:]))))
		answer1_found = True

	elf1_idx = (elf1_idx + 1 + elf1_recipe) % recipes_len
	elf2_idx = (elf2_idx + 1 + elf2_recipe) % recipes_len
