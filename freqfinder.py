import os
from datetime import datetime

files = os.listdir()

now = datetime.now()
nowstring = now.strftime("%Y-%m-%d %H-%M-%S")

outfilename = f"out from {nowstring}.txt"

outfile = open(outfilename, "w")

for file in files:
	if file.endswith(".txt") and not file.startswith("out from"):
		f = open(file, "r")

		firstline = True

		max_level = -1000.0
		corr_freq = 0.0

		for line in f:
			if firstline:
				firstline = False
			else:
				freq, level = line.strip().split("\t")
				freq = float(freq)
				level = float(level)
				if level > max_level:
					max_level = level 
					corr_freq = freq
		experiment = file.split(".txt")[0]
		outfile.write(f"\"{experiment}\" max level = {max_level}, corresponding freq = {corr_freq}.\n")

outfile.close()


