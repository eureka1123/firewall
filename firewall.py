import csv
class Firewall:
	def __init__(self, path):
		#self.rules is in the format: {direction:{protocol:{{all ports},port:{all ip_addresses}}}}
		self.rules = {}
		with open(path,"r") as f:
			reader = csv.reader(f, delimiter=',') 
			for l in reader:
				port = tuple(l[2].split("-"))
				if len(port)==1:
					port = int(port[0])
				ip = tuple(l[3].split("-"))
				if len(ip)==1:
					ip = ip[0]
				self.rules.setdefault(l[0],{}).setdefault(l[1],[set(),{}])
				self.rules[l[0]][l[1]][0].add(port)
				self.rules[l[0]][l[1]][1].setdefault(port,set()).add(ip)

	def check_ip(self, ip_address, filtered_port):
		"""
		check if desired ip address exists in rules (which already satisfy all other parameters)
		"""
		#check in set first in case it exists not in a range
		if ip_address in filtered_port:
			return True
		#could also exist in range of ip addresses in rules
		else:
			for ip in filtered_port:
				if type(ip)==tuple:
					ip_orig = ip_address.split(".")
					ip_start = ip[0].split(".")
					ip_end = ip[1].split(".")
					#checks if each of the octets in the desired ip address is within range of the 
					#corresponding octets of ip_start and ip_end 
					if all([True if ip_start[i]<=ip_orig[i]<=ip_end[i] else False for i in range(4)]):
						return True
		return False

	def accept_packet(self, direction, protocol, port, ip_address):
		if direction in self.rules:
			filtered_direction = self.rules[direction]
			if protocol in filtered_direction:
				filtered_protocol = filtered_direction[protocol]
				#check in set first in case it exists not in a range
				if port in filtered_protocol[0]:
					filtered_port = filtered_protocol[1][port]
					if self.check_ip(ip_address, filtered_port):
						return True
				#could also exist in range of ports in rules
				for p in filtered_protocol[1]:
					if type(p)==tuple and int(p[0])<=port<=int(p[1]):
						filtered_port = filtered_protocol[1][p]
						if self.check_ip(ip_address, filtered_port):
							return True
		return False