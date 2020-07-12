import operator
import os
import tabulate

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

def site_login():
	driver.get('http://192.168.0.1') # probably the url
	# use environment variable if exists, or 'admin' password by default
	driver.find_element_by_id('admin_Password').send_keys(os.getenv('DLINK_PASS', 'admin'))
	driver.find_element_by_id('logIn_btn').click()
	driver.find_element_by_id('client_image').click()
	clients = driver.find_elements_by_class_name('client_Tag')
	return [transform(client) for client in clients]

def transform(e):
	sub = e.find_elements_by_css_selector('*')
	info = sub[1].find_elements_by_css_selector('*')
	obj = {
		'name': info[0].text,
		'ip': info[3].text,
		'connection': 'Ethernet' if sub[0].get_attribute('class') == 'link_IconE_Allow' else 'WiFi'
	}
	vendor = info[2].text
	if vendor != 'Unknown Vendor':
		obj['vendor'] = vendor
	return obj

if __name__ == '__main__':
	chrome_options = Options()
	chrome_options.add_argument('headless')

	driver = webdriver.Chrome(options=chrome_options)
	driver.implicitly_wait(2)
	L = site_login()
	driver.close()

	L.sort(key=operator.itemgetter('ip', 'name'))
	header = L[0].keys()
	rows = [x.values() for x in L]

	print(tabulate.tabulate(rows, header))
