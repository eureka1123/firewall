from random import randint
import csv
def create_rules():
	rules = []
	for i in range(50000):
		entry = []
		if i%2:
			entry.append("inbound")
			entry.append("tcp")
		else:
			entry.append("outbound")
			entry.append("udp")
		start = randint(1,65535)
		end = randint(start,65535)
		entry.append(str(start)+"-"+str(end))
		start1 = randint(0,255)
		start2 = randint(0,255)
		start3 = randint(0,255)
		start4 = randint(0,255)
		end1 = randint(start1,255)
		end2 = randint(start2,255)
		end3 = randint(start3,255)
		end4 = randint(start4,255)
		entry.append(".".join([str(start1),str(start2),str(start3),str(start4)])\
					+"-"+".".join([str(end1),str(end2),str(end3),str(end4)]))
		rules.append(entry)
	#from https://stackoverflow.com/questions/14037540/writing-a-python-list-of-lists-to-a-csv-file
	with open("rules_extended.csv", "w") as f:
		writer = csv.writer(f)
		writer.writerows(rules)

