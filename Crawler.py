from bs4 import BeautifulSoup
import requests
import time
import re

import sys

sys.path.append('/home/florian/anaconda3/lib/python3.7/site-packages')

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class Crawler():

    def crawlData(self, WebUrl, rewUrl):

        # soup get rewards

        request_Rew = requests.get(rewUrl)
        doc = BeautifulSoup(request_Rew.text, 'html.parser')

        numOfRewards = 0
        for card in doc.select('.hover-group'):
            numOfRewards = numOfRewards + 1

        # selenium scroll page

        browser = webdriver.Chrome('./ChromeDriver/chromedriver')
        browser.get(WebUrl)

        time.sleep(1)

        elem = browser.find_element_by_tag_name("body")
        no_of_pagedowns = 12

        while no_of_pagedowns:
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)
            no_of_pagedowns -= 1

        # number of pictures

        project_image = browser.find_elements_by_css_selector('[alt*="Project image"]')
        post_elems = browser.find_elements_by_xpath("//figure/img")
        allImages = project_image + post_elems

        numOfImages = len(allImages)

        # has video

        hasVideo = False

        video = browser.find_elements_by_tag_name("video")

        if len(video) > 0:
            hasVideo = True

        # Length of Text
        texts = []
        text_Length = 0

        paragraphs = browser.find_elements_by_xpath("//section[@class='project-content']//p")
        for paragraph in paragraphs:
            text = str(paragraph.text)
            text_Length = text_Length + len(text)
            texts.append(text)

        # facebook friends
        hasFacebook = False
        numOfFbFriends = False

        button = browser.find_element_by_xpath("//div[@id='experimental-creator-bio']/button")
        button.click()
        links = browser.find_elements_by_link_text('facebook.com')

        if len(links) > 0:
            hasFacebook = True
            for link in links:
                fbLink = link.get_attribute("href")
            request_FB = requests.get(fbLink)
            fbSoup = BeautifulSoup(request_FB.text, 'html.parser')
            classAbo = fbSoup.findAll('div', text = re.compile('haben das abonniert'))
            stringifyText = str(classAbo[1].text)
            numOfFbFriends_Array = [int(s) for s in stringifyText.split() if s.isdigit()]
            numOfFbFriends = numOfFbFriends_Array[0]

        return numOfImages, numOfRewards, hasVideo, texts, text_Length, hasFacebook, numOfFbFriends










