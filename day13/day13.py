import os
import time

base_file = os.path.splitext(__file__)[0]

track_map = []

with open(base_file + ".input", "r") as fo:
	for line in fo:
		row = []
		for cell in line.rstrip():
			row.append(cell);
		track_map.append(row)

directions = "<^>v"
direction_paths = "-|-|"
turn_map= {"<\\": 1, "</": 3, ">\\": 3, ">/": 1, "^\\": 0, "^/": 2, "v\\": 2, "v/": 0}

carts = []

for y, row in enumerate(track_map):
	for x, cell in enumerate(row):
		if track_map[y][x] in directions:
			carts.append([directions.index(cell), x, y, 0, direction_paths[directions.index(cell)]])

# Cart structure [current direction, x, y, next turn, current_path_replacement]

def junction_turn(cart):
	if cart[3] == 0: # turn left
		return ((cart[0] - 1) % 4, 1)
	elif cart[3] == 1: # go straight
		return (cart[0], 2)
	elif cart[3] == 2: # turn right
		return ((cart[0] + 1) % 4, 0)


def tick():
	collisions = []

	for i, cart in enumerate(carts):
		collision = False
		x = cart[1]
		y = cart[2]

		if (cart[1], cart[2]) in collisions: # Skip moving cart in collision, will be garbage collected after tick
			continue

		track_map[y][x] = cart[4] # Restore map at previous location

		cart_direction = cart[0]

		if cart_direction == 0: # <
			dx = -1
			dy = 0
		elif cart_direction == 2: # >
			dx = 1
			dy = 0
		elif cart_direction == 1: # ^
			dx = 0
			dy = -1
		else: # v
			dx = 0
			dy = 1

		next_cell = track_map[y + dy][x + dx]
		carts[i][4] = next_cell
		carts[i][1] += dx
		carts[i][2] += dy

		if next_cell in "-|":
			pass
		elif next_cell in "\\/":
			carts[i][0] = turn_map[directions[cart_direction] + next_cell]
		elif next_cell == "+":
			direction, next_turn = junction_turn(cart)
			carts[i][0] = direction
			carts[i][3] = next_turn
		else: # collision
			collision = True
			track_map[y + dy][x + dx] = "X"
			collisions.append((x + dx, y + dy))

		if not collision:
			track_map[y + dy][x + dx] = directions[carts[i][0]]

	carts.sort(key=lambda pt: (pt[1], pt[2]))
	return collisions


collisions = []
first_collision = False

while True:
	while collisions == []:
		collisions = tick()

	if not first_collision:
		first_collision = True
		print("First crash happens at %u,%u" %(collisions[0][0], collisions[0][1]))

	# Clear up collisions
	for collision in collisions:
		colliding_carts = list(filter(lambda cart: cart[1] == collision[0] and cart[2] == collision[1], carts))

		for cart in colliding_carts:
			if cart[4] not in directions:
				track_map[collision[1]][collision[0]] = cart[4]
		carts = list(filter(lambda cart: not (cart[1] == collision[0] and cart[2] == collision[1]), carts))

	collisions = []

	if len(carts) == 1:
		break

print("The location of the last cart is %u,%u" % (carts[0][1], carts[0][2]))