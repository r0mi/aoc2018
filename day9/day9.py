import sys
import time
from collections import deque

NUM_PLAYERS = 459
MARBLES = 71320
SECOND_ROUND_MARBLES = MARBLES * 100
PROGRESS_BAR_LENGTH = 80

def show_progress(progress, duration):
	blocks = int(round(PROGRESS_BAR_LENGTH * progress))
	sys.stdout.write("\r[{0}] {1:3d}% | {2}".format( "#" * blocks + "-" * (PROGRESS_BAR_LENGTH - blocks), round(progress * 100), "%2u:%02u" % (duration / 60, duration % 60)))
	sys.stdout.flush()


def play(marbles):
	current_idx = 0
	circle = deque([0], maxlen=marbles)
	players = [0 for x in range(NUM_PLAYERS)]
	marble = 1
	player = 0
	start_time = time.time()
	length = 1

	while marble <= marbles:
		points = 0

		if marble % 23:
			current_idx += 2

			if current_idx == length:
				circle.append(marble)

			else:
				current_idx = current_idx % length
				circle.rotate(length - current_idx)
				circle.append(marble)
				current_idx = length

			length += 1
		else:
			points = points + marble
			circle.rotate(-(current_idx - 7))
			points = points + circle.popleft()
			current_idx = 0
			length -= 1

		if points:
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
