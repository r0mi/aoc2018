import os
import re
from datetime import datetime, timedelta

base_file = os.path.splitext(__file__)[0]

regex = re.compile(r"\[(?P<datetime>.*)\] ((?P<sleep>falls asleep)|(?P<wakeup>wakes up)|(?P<guard>Guard #(?P<id>\d+) .*))")

schedule = []

with open(base_file + ".input", "r") as fo:
	for line in fo:
		schedule.append(line.rstrip())

schedule.sort()

with open(base_file + "_sorted.output", "w") as fo:
	for item in schedule:
		fo.write(item + "\n")

guard_sleeps = dict()
current_guard = ""
fell_asleep = False

for entry in schedule:
	match = regex.search(entry)
	if match:
		dt = datetime.strptime(match.group('datetime'), "%Y-%m-%d %H:%M")
		if match.group('id'):
			current_guard = match.group('id')
			fell_asleep = False

			if dt.hour > 0:
				dt = dt + timedelta(days=1)

			if current_guard not in guard_sleeps:
				guard_sleeps[current_guard] = {"total_minutes_slept": 0, "on_duty": {dt.strftime('%m-%d'): []} }
			else:
				guard_sleeps[current_guard]["on_duty"][dt.strftime('%m-%d')] = []
		elif match.group('sleep'):
			fell_asleep = dt.minute
		elif match.group('wakeup'):
			date = dt.strftime('%m-%d')
			guard_sleeps[current_guard]["on_duty"][date].append((fell_asleep, dt.minute))
			guard_sleeps[current_guard]["total_minutes_slept"] = guard_sleeps[current_guard]["total_minutes_slept"] + dt.minute - fell_asleep

with open(base_file + "_guard_sleeps.output", "w") as fo:
	fo.write("Date   ID     Minute\n")
	fo.write("              " + "".join([c * 10 for c in "012345"]) + "\n")
	fo.write("              " + "0123456789" * 6 + "\n")
	for guard, sleeps in guard_sleeps.items():
		for date, intervals in sleeps["on_duty"].items():
			fo.write(date + "  " + "#%4s" % guard + "  ")
			last_awake = 0
			for sleep_interval in intervals:
				fo.write("." * (sleep_interval[0] - last_awake))
				fo.write("#" * (sleep_interval[1] - sleep_interval[0]))
				last_awake = sleep_interval[1]
			fo.write("." * (60 - last_awake) + "\n")
		fo.write("Total minutes slept " + str(sleeps["total_minutes_slept"]) + "\n\n")

sorted_by_total_minutes = sorted(guard_sleeps.items(), key=lambda kv: kv[1]['total_minutes_slept'], reverse=True)
s1_guard = sorted_by_total_minutes[0]

histogram = dict(zip(range(0,60), [0]*60))

for date, sleeps in s1_guard[1]['on_duty'].items():
	for sleep in sleeps:
		for x in range(*sleep):
			histogram[x] = histogram[x] + 1

s1_minute = max(histogram, key=histogram.get)

print("Strategy 1: guard #%s, minute %u. Answer %u" % (s1_guard[0], s1_minute, s1_minute * int(s1_guard[0])))

s2_guard = None
s2_minute = None
sleep_count = 0

for guard, sleeps in guard_sleeps.items():
	histogram = dict(zip(range(0, 60), [0] * 60))

	for date, intervals in sleeps["on_duty"].items():
		for sleep in intervals:
			for x in range(*sleep):
				histogram[x] = histogram[x] + 1

	most_frequent_minute = max(histogram, key=histogram.get)

	if histogram[most_frequent_minute] > sleep_count:
		sleep_count = histogram[most_frequent_minute]
		s2_minute = most_frequent_minute
		s2_guard = int(guard)

print("Strategy 2: guard #%u, minute %u. Answer %u" % (s2_guard, s2_minute, s2_minute * s2_guard))
