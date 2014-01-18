import p2p

if __name__=='__main__':
	p = p2p.p2p()
	port = 5566
	if p.bind(port):
		print ('[+] Listen on port %d Success'%port)
		p.p2pserver()
