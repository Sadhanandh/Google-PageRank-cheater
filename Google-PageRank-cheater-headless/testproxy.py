#import urllib2
#proxy = urllib2.ProxyHandler({'http': 'http://127.0.0.1:9050'})
#opener = urllib2.build_opener(proxy)
#urllib2.install_opener(opener)
#r = urllib2.urlopen('http://ifconfig.me')
#print r.read()

def getip():
	import pycurl
	c = pycurl.Curl()

	import cStringIO
	buf = cStringIO.StringIO()

	c.setopt(pycurl.PROXY, '127.0.0.1')
	c.setopt(pycurl.PROXYPORT, 9050)
	c.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5)
	c.setopt(c.WRITEFUNCTION, buf.write)
	c.setopt(c.URL, 'http://ifconfig.me')
	c.perform()
	data = buf.getvalue()
	import re
	ip = re.findall(".*?ip_address.*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*",data,re.I)
	if len(ip)>0:
		ip = ip[0]
	else :
		ip = "Not found!"
	print ip

if __name__ == "__main__":
	getip()
	import browsermod
	browsermod.changeip()
	getip()

