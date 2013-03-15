#! /usr/bin/env python
import os
import re
import random
import time
import mechanize
import cookielib
import telnetlib
import socks
import socket
import urllib2
from TorCtl import TorCtl

query_word = "hello"
s_url = "http://en.wikipedia.org/wiki/HelloWorld"
max_n =10
min_rand = 2
max_rand = 10
max_rand+=1
min_rand_UA = 2
max_rand_UA = 10
max_rand_UA+=1


__originalSocket = socket.socket
__originalCreateConnection = socket.create_connection
#
#Read config file
#Read UA file

# Browser
def create_connection(address, timeout=None, source_address=None):
	sock = socks.socksocket()
	sock.connect(address)
	return sock

def cheatgoogle(query_word,s_url,max_n,min_rand,max_rand,UA,using_tor,tor_u_port):


	if using_tor:
		socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", tor_u_port)
		# patch the socket module
		socket.socket = socks.socksocket
		socket.create_connection = create_connection

	br = mechanize.Browser()
	cj = cookielib.LWPCookieJar()
	br.set_cookiejar(cj)
	br.set_handle_equiv(True)
	#br.set_handle_gzip(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)
	br.set_handle_robots(False)
	br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
	#UA =  'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'
	br.addheaders = [('User-agent',UA), ('Accept', '*/*')]
# random.randrange(min_rand_UA,max_rand_UA)
	br._factory.is_html = True

	#req = mechanize.Request("http://www.google.com")
	#req.set_proxy("localhost:8888","http")
	#mechanize.urlopen(req)

	#ifc = br.open("http://ifconfig.me")
	#ip_address.*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})
 	#ip = re.findall(".*?ip_address.*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*",ifc.read(),re.I)
	#if len(ip) > 0:
	#	ip=ip[0]
	#else:
	#	ip = "Not Found"
	ifc = br.open("http://icanhazip.com")
	print ""
	print "Your IP :" + ifc.read()
	print ""
	res1 = br.open("http://www.google.com")

	try:
		br.select_form(nr=0)
		br.form["q"]=query_word
		res2 = br.submit()
	#except Exception as e:
	#except mechanize._response.httperror_seek_wrapper as e:
	except urllib2.HTTPError as e:
		print e
		print "This IP has been blacklisted by google."
		print "Google redirected me to its captcha page :( "
		print "Im unable to procede with this request."
		print "Lemme change the IP and try again."
		return 1
	print "_"
	print "Cookie:" , str(res2.info()).split("\n")[4]
	print " "
	time.sleep(1)
	#raw_input()
	html = res2.read()
	if not os.path.exists("files"):
		os.makedirs("files")
	f = open("files/"+"Page1.html","w")
	f.write(html)
	f.close()

	found = False
	for page_n in range(1,max_n+1):
		s_num = (page_n+1)*10
		for link in br.links():
			print link.url
			if re.findall(".*"+s_url+".*",link.url):
				res1 = br.follow_link(url_regex=".*"+s_url+".*")
				html = res1.read()
				f = open("files/"+"Page"+str(page_n)+".html","w")
				f.write(html)
				f.close()
				print ""
				print "The link "+s_url +" has been found."
				print "Found at page ",
				print page_n
				print ""
				found = True
				break
				
		else:
			try:
				res1=br.follow_link(url_regex="^.*\&start="+str(s_num)+"\&sa=N$")
				html = res1.read()
				f = open("files/"+"Page"+str(page_n)+".html","w")
				f.write(html)
				f.close()
			except mechanize._mechanize.LinkNotFoundError as e: 
				print "error!!!"+e
				break

		print "_--------_"
		print "_--------_"
		print "_--------_"
		print "The Next Link is -----",
		print br.geturl()
		print "_--------_"
		print "_--------_"
		

		if found == True:
			print "Clicking the url at page :" + str(page_n)
			print ""
			print "Success!  The link has been clicked."
			print ""
			break
		print ""
		print "Waiting for some random seconds:"
		r_t = random.randrange(min_rand,max_rand)
		print r_t ,"Sec/s"
		print "" 
		time.sleep( r_t)
	else:
		print ""
		print "Not found in any of the "+str(max_n)+" pages."
	return 0

def changeiptelnet(host="localhost",port=9051,passphrase=""):
	#import telnetlib
	print host ,port 
 	socket.socket = __originalSocket
	socket.create_connection = __originalCreateConnection
	tn = telnetlib.Telnet(host,port,5)
	tn.read_until("Escape character is '^]'.", 2)
	tn.write('AUTHENTICATE "'+passphrase+'"\r\n')
	resp = tn.read_until("250 OK", 2)
	if not resp.strip("\r\n") == "250 OK":
		print "error with tor Auth"
	tn.write("signal NEWNYM\r\n")
	resp = tn.read_until("250 OK", 2)
	if not resp.strip("\r\n") == "250 OK":
		print "error with tor"
	tn.write("quit\r\n")
	tn.close()
	socket.socket = socks.socksocket
	socket.create_connection = create_connection

	time.sleep(5)



def changeip(host="localhost",port=9051,passphrase=""):
	#from TorCtl import TorCtl
	#conn = TorCtl.connect()

 	socket.socket = __originalSocket
	socket.create_connection = __originalCreateConnection

	conn = TorCtl.connect(controlAddr=host, controlPort=port, passphrase=passphrase)
	conn.send_signal(0x03) #NEWNYMRN
	#conn.send_signal("NEWNYM")
	#conn.sendAndRecv('signal newnymrn')
	#conn.close()
	socket.socket = socks.socksocket
	socket.create_connection = create_connection
	time.sleep(5)
