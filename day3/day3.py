import os
import re

base_file = os.path.splitext(__file__)[0]

claims_raw = []

with open(base_file + ".input", "r") as fo:
    for line in fo:
        claims_raw.append(line.rstrip())

claim_re = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")

claims = []
width = 0
height = 0
for claim in claims_raw:
	match = claim_re.search(claim)
	if match:
		i = int(match.group(1))
		left = int(match.group(2))
		top = int(match.group(3))
		w = int(match.group(4))
		h = int(match.group(5))
		claims.append({"id": i, "left": left, "top": top, "width": w, "height":h, "overlapping": False})
		if left + w > width:
			width = left + w
		if top + h > height:
			height = top + h
	else:
		print("Error parsing ", c)

print("Fabric dimensions %ix%i" % (width, height))

canvas = [[0 for x in range(width + 1)] for y in range(height + 1)]
overlapping = 0

for i in range(len(claims)):
	for x in range(claims[i]['left'], claims[i]['left'] + claims[i]['width']):
		for y in range(claims[i]['top'], claims[i]['top'] + claims[i]['height']):
			if canvas[x][y] == 0:
				canvas[x][y] = claims[i]["id"]
			elif type(canvas[x][y]) == int:
				claims[i]['overlapping'] = True
				claims[ canvas[x][y] - 1 ]['overlapping'] = True
				canvas[x][y] = set([canvas[x][y], claims[i]["id"]])
				overlapping = overlapping + 1
			else:
				claims[i]['overlapping'] = True
				canvas[x][y].add(claims[i]["id"])

print("Overlapping", overlapping, "square inches")

print("Intact claim ID", list(filter(lambda x: not x['overlapping'], claims))[0]['id'])
