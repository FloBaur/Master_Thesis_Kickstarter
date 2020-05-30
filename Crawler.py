from bs4 import BeautifulSoup
import requests
import time

import sys

sys.path.append('/home/florian/anaconda3/lib/python3.7/site-packages')

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Crawler():

    def crawlData(self, WebUrl, rewUrl):

        request_Rew = requests.get(rewUrl)
        doc = BeautifulSoup(request_Rew.text, 'html.parser')

        numOfRewards = 0
        for card in doc.select('.hover-group'):
            numOfRewards = numOfRewards + 1
        stop = True
        browser = webdriver.Chrome()
        browser.get(WebUrl)
        time.sleep(1)


        elem = browser.find_element_by_tag_name("body")
        no_of_pagedowns = 20



        while no_of_pagedowns:
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)
            no_of_pagedowns-=1

        post_elems = browser.find_elements_by_class_name("lazyloaded")



        request_Web = requests.get(WebUrl)
        webDoc = BeautifulSoup(request_Web.text, 'html.parser')

        numOfPics = 0

        for img in webDoc.select(".lazyloaded"):
            numOfPics = numOfPics + 1





