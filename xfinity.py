from enum import Enum
import time

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys

ROUTER = 'http://10.0.0.1'
USERNAME = 'admin'
PASSWORD = ''

# could the values be the string representing them in the UI and use enum.parse to get vs get_connection() ?
class Connection(Enum):
    ETHERNET = 1
    WIFI_2G = 2
    WIFI_5G = 3
    UNKNOWN = 4

class Device:
    def __init__(self, td, is_online):
        self.is_online = is_online
        self.host = td[0].text
        self.is_dhcp = td[1].text == 'DHCP'
        self.connection = Device.get_connection(td[3 if is_online else 2].text)
        self.rssi = Device.get_rssi(td[2].text) if is_online else 0
        self.mac = Device.get_mac(td[0])
        self.ipv4 = Device.get_ipv4(td[0])

    def __str__(self):
        icon = '+' if self.is_online else '-'
        return f'{icon} {self.host} | {self.rssi}'

    @staticmethod
    def get_rssi(rssi_text):
        if rssi_text == 'NA':
            return 0
        return int(rssi_text[:-4])

    @staticmethod
    def get_connection(connection_text):
        if connection_text == 'Ethernet':
            return Connection.ETHERNET
        elif connection_text == 'Wi-Fi 2.4G':
            return Connection.WIFI_2G
        elif connection_text == 'Wi-Fi 5G':
            return Connection.WIFI_5G
        return Connection.UNKNOWN

    @staticmethod
    def get_mac(td):
        return ''
    
    @staticmethod
    def get_ipv4(td):
        for dd in td.find_elements_by_tag_name('dd'):
            print(dd.text)
        return ''

def extract_devices(table, is_online):
    # Skips header and footer in table
    for tr in table.find_elements_by_tag_name('tr')[1:-1]:
        td = tr.find_elements_by_tag_name('td')
        devices.append(Device(td, is_online))

devices = []

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('--log-level=3')

with Chrome(options=options) as driver:
    driver.get(ROUTER)

    # Login
    driver.find_element_by_id('username').send_keys(USERNAME)
    driver.find_element_by_id('password').send_keys(PASSWORD)
    driver.find_element_by_css_selector('input.btn').click()

    # Devices Page
    while(True):
        driver.get(ROUTER + '/connected_devices_computers.php')

        tables = driver.find_elements_by_css_selector('table.data')

        extract_devices(tables[0], True)
        extract_devices(tables[1], False)

        for device in sorted(devices, key=lambda x: x.rssi, reverse=True):
            print(device)

        devices = []
        time.sleep(10)
