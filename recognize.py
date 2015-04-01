import csv

with open("./sentence.hmm", "rb") as infile:
	reader = csv.reader(infile, delimiter=" ")
	for row in reader:
		print row