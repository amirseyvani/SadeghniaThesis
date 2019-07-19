import time
import bs4
import re
from selenium import webdriver
import traceback
import unidecode
import io

def get_driver(driver_width=600, driver_height=300, limit=300):
    connections_attempted = 0
    while connections_attempted < limit:
        try:
            driver = webdriver.Chrome('chromedriver.exe')
            driver.set_window_size(driver_width, driver_height)
            return driver
        except Exception as e:
            connections_attempted += 1
            print('Getting driver again...')
            print('  connections attempted: {}'.format(connections_attempted))
            print('  exception message: {}'.format(e))
            traceback.print_exc()
