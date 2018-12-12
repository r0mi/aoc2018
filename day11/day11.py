import os
import sys
import time
import multiprocessing as mp

GRID_SERIAL_NUMBER = 9005
FUEL_GRID_TOTAL_SIZE = 300
FUEL_GRID_SIZE = 3
PROGRESS_BAR_LENGTH = int(FUEL_GRID_TOTAL_SIZE / 4)

base_file = os.path.splitext(__file__)[0]

power_grid = [[0 for x in range(FUEL_GRID_TOTAL_SIZE + 1)] for y in range(FUEL_GRID_TOTAL_SIZE + 1)]

def show_progress(progress, duration, status):
	blocks = int(round(PROGRESS_BAR_LENGTH * progress))
	sys.stdout.write("\r[{0}] {1:3d}% | {2} | {3}".format( "#" * blocks + "-" * (PROGRESS_BAR_LENGTH - blocks), round(progress * 100), "%2u:%02u" % (duration / 60, duration % 60), status))
	sys.stdout.flush()

def cell_power(x, y):
	rack_id = x + 10
	starting_power_level = (rack_id * y + GRID_SERIAL_NUMBER) * rack_id
	if starting_power_level > 100:
		return int(str(starting_power_level)[-3]) - 5
	else:
		return -5

def grid_power(start_x, start_y, size):
	global power_grid
	total_power = 0
	for x in range(start_x, start_x + size):
		for y in range(start_y, start_y + size):
			total_power = total_power + power_grid[x][y]
	return total_power


def search_highest_grid_power(square_size):
	highest_total_power = -1000
	highest_total_power_cell_top_left_coordinates = None

	for start_x in range(1, FUEL_GRID_TOTAL_SIZE - square_size + 1):
		for start_y in range(1, FUEL_GRID_TOTAL_SIZE - square_size + 1):
			power = grid_power(start_x, start_y, square_size)
			if power > highest_total_power:
				highest_total_power = power
				highest_total_power_cell_top_left_coordinates = (start_x, start_y)

	return (highest_total_power, highest_total_power_cell_top_left_coordinates, square_size)

# Precalculate grid power levels
for x in range(1, FUEL_GRID_TOTAL_SIZE):
	for y in range(1, FUEL_GRID_TOTAL_SIZE):
		power_grid[x][y] = cell_power(x, y)

power, coordinates, _ = search_highest_grid_power(FUEL_GRID_SIZE)

print("X,Y coordinate of the top left fuel cell of the %ux%u matrix with the largest total power (%u) on a grid with serial number of %u is (%u, %u)" % (FUEL_GRID_SIZE, FUEL_GRID_SIZE, power, GRID_SERIAL_NUMBER, coordinates[0], coordinates[1]))

total_calculations = 0
for size in range(1, FUEL_GRID_TOTAL_SIZE):
	total_calculations = total_calculations + size * size * (FUEL_GRID_TOTAL_SIZE - size + 1) * (FUEL_GRID_TOTAL_SIZE - size + 1)

print("Searching for optimal grid size ...")

pool = mp.Pool() # default uses multiprocessing.cpu_count()
start_time = time.time()
best_results = (0,)
worse_results = 0
completed_calculations = 0

results = [pool.apply_async(search_highest_grid_power, args=(grid_size,)) for grid_size in range(1, FUEL_GRID_TOTAL_SIZE)]

fo = open(base_file + ".output", "w")

for result in results:
	power, coordinates, size = result.get()

	if best_results[0] < power:
		best_results = (power, coordinates, size)
		worse_results = 0
	else:
		worse_results +=1

	fo.write("Size %2u, power %3d\n" % (size, power))

	status = "Best power %3u starting @ (%3u, %3u) with size %d/%d" % (best_results[0], best_results[1][0], best_results[1][1], best_results[2], size)
	completed_calculations = completed_calculations + size * size * 1.0 * (FUEL_GRID_TOTAL_SIZE - size + 1) * (FUEL_GRID_TOTAL_SIZE - size + 1)
	show_progress(completed_calculations / total_calculations, time.time() - start_time, status)

	if worse_results > 5:
		pool.terminate()
		print()
		break

else:
	print()

fo.close()

print("X,Y,size of square with the largest total power (%u) is %u,%u,%u" % (best_results[0], best_results[1][0], best_results[1][1], best_results[2]))
