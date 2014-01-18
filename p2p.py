import socket

class pair:
	key = 0
	value = 0
	def __init__(self,key,value):
		self.key = key
		self.value = value

	def __eq__(self,other):
		if self.key == other.key:
			self.value2 = other.value
			other.value2 = self.value
		return self.key == other.key

	def __hash__(self):
		return hash(self.key)

import string

def string2addr(addr_str):
	addr,port_str = addr_str.split(':')
	port = string.atoi(port_str)
	if 0<port and port < 65536:
		return addr,port
	return False

class p2p:
	pair_set = 0
	udp_socket = 0

	p2phead = 'p2p:'
	p_addr=0
	buf_size = 8192

	def __init__(self):
		self.pair_set = set()
		self.udp_socket = 0

	def close(self):
		if self.udp_socket:
			self.udp_socket.close()
			self.udp_socket = 0

	def bind(self,port):
		self.close()
		try:
			self.udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
			self.udp_socket.bind(('0.0.0.0',port))
			self.udp_socket.setblocking(0)
		except:
			self.close()
		return self.udp_socket

	def p2pserver(self):
		try:
			while(self.udp_socket):
				try:
					data,addr = self.udp_socket.recvfrom(self.buf_size)
					if data[0:len(self.p2phead)] == self.p2phead:
						p = pair(data,addr)
						ip,port = addr
						link_str = "%s@%s:%d"%(data,ip,port)
						if p not in self.pair_set:
							self.pair_set.add(p)
							print ('[+] %s add'%link_str)
						else:
							addr2 = p.value2
							addr_str1 = self.p2phead+'%s:%d'%addr
							addr_str2 = self.p2phead+'%s:%d'%addr2
							self.udp_socket.sendto(addr_str1,addr2)
							self.udp_socket.sendto(addr_str2,addr)
							self.pair_set.remove(p)
							print ('[+] %s complete'%link_str)
				except:
					pass
		except KeyboardInterrupt:
			print ('[+] Accept Ctrl+C..Quit')
			self.close()

	def p2pconnect(self,server_addr,p2pcode):
		if not self.udp_socket:
			return False
		send = self.p2phead+p2pcode;
		self.udp_socket.sendto(send,server_addr)
		try:
			while(self.udp_socket):
				try:
					data,addr = self.udp_socket.recvfrom(self.buf_size)
					if data[0:len(self.p2phead)] == self.p2phead:
						self.p_addr = string2addr(data[len(self.p2phead):len(data)])
						if self.p_addr:
							print ('[+] Making Tunnel %s'%data)
							self.udp_socket.sendto('',self.p_addr)
							return True
				except:
					pass
		except KeyboardInterrupt:
			print ('[+] Accept Ctrl+C..Quit')
			self.close()
		return False

	def p2psend(self,data):
		if not self.udp_socket:
			return False
		return self.udp_socket.sendto(data,self.p_addr)

	def p2precv(self):
		if not self.udp_socket:
			return False
		data = 0
		try:
			data = self.udp_socket.recvfrom(self.buf_size)
		except:
			pass
		return data


