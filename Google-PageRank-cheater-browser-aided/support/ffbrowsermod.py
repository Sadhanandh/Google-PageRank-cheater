#! /usr/bin/env python
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import random
import os

word_n = "hello"
search_link_w = "hellopoetry.com"
max_n = 5
iter_n = 1
min_t =2
max_t = 3

def cheatgoogleff(word_n,search_link_w,max_n,iter_n,min_t,max_t):
	fp = webdriver.FirefoxProfile(os.path.join(os.path.abspath("."),'support/User-Agents/UA'+str(iter_n)))
	browser = webdriver.Firefox(fp) # Get local session of firefox
	browser.get("http://ifconfig.me") # Load page
	time.sleep(3)

	browser.get("http://www.google.com") # Load page
	elem = browser.find_element_by_name("q")
	elem.send_keys(word_n + Keys.RETURN)
	for x in range(max_n):
		#time.sleep(2)
		time.sleep(random.randrange(min_t,max_t))
		try :
			e = browser.find_element_by_xpath("//a[contains(@href,'"+search_link_w+"')]")
			e.click()
			print "Found the link @ "+str(x+1)+" Page"
			break
		except NoSuchElementException as e:
			#elem = browser.find_element_by_id("pnnext")
			elem = browser.find_element_by_xpath("//a[contains(@href,'&start="+str(10*(x+1))+"&sa=N')]")
			elem.click()

	else:
		print "Didnt find the Url in any of the "+str(max_n)+" Pages."

	#browser.close()
	
if __name__ == '__main__':

	cheatgoogleff(word_n,search_link_w,max_n,iter_n,min_t,max_t)
