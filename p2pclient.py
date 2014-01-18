import p2p
import random
import threading
import string

def getdata(p):
	while True:
		line =p.p2precv()
		print (line)

if __name__=='__main__':
	p = p2p.p2p()
	port = random.randint(1,65535)
	if p.bind(port):
		print ('[+] Listen on port %d Success'%port)
		ip = raw_input('ip:')
		port_str = raw_input('port:')
		port = string.atoi(port_str)
		server_addr = (ip,port)
		code = 'Tarantula'
		if p.p2pconnect(server_addr,code):
			print ('Connect Success')
			p.udp_socket.setblocking(1)
			t = threading.Thread(target=getdata,args=(p,))
			t.setDaemon(True)
			t.start()
			while True:
				line = raw_input()
				p.p2psend(line)



