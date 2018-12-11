import sys
import time

NUM_PLAYERS = 459
MARBLES = 71320
SECOND_ROUND_MARBLES = MARBLES * 100
PROGRESS_BAR_LENGTH = 80

def show_progress(progress, duration):
	blocks = int(round(PROGRESS_BAR_LENGTH * progress))
	sys.stdout.write("\r[{0}] {1:3d}% | {2}".format( "#" * blocks + "-" * (PROGRESS_BAR_LENGTH - blocks), round(progress * 100), "%2u:%02u" % (duration / 60, duration % 60)))
	sys.stdout.flush()

def take_turn(circle, marble, index):
	points = 0
	if marble % 23:
		index = index + 2

		if len(circle) == 1:
			index = 1
			circle.append(marble)

		elif index == len(circle):
			circle.append(marble)

		else:
			index = index % len(circle)
			circle.insert(index, marble)

	else:
		points = points + marble
		index = index - 7
		points = points + circle.pop(index)

		if index < 0:
			index = index + 1 % len(circle)

	return (circle, index, points)

def play(marbles):
	current_idx = 0
	circle = [0]
	players = [0 for x in range(NUM_PLAYERS)]
	marble = 1
	player = 0
	start_time = time.time()

	while marble <= marbles:
		circle, current_idx, points = take_turn(circle, marble, current_idx)
		players[player] = players[player] + points
		marble = marble + 1
		player = (player + 1) % NUM_PLAYERS

		if marble % 10000 == 0:
			show_progress(marble * 1.0 / marbles, time.time() - start_time)

	# Game finished
	show_progress(marble * 1.0 / marbles, time.time() - start_time)
	print()
	print("Winning Elf's score is", max(players))

print("Playing with %u marbles" % MARBLES)
play(MARBLES)

print("\nPlaying with %u marbles" % SECOND_ROUND_MARBLES)
play(SECOND_ROUND_MARBLES)
