from q3 import set1_3

def set1_4(filename):
	with open(filename) as fp:
		line = fp.readline()
		# print(line)
		line = line[:-1]
		# print(line)
		# print("ddddddd")
		while (line):
			print(set1_3(line))
			line = fp.readline()
			line = line[:-1]

set1_4("set1_4.txt")