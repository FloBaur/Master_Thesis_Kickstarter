from bs4 import BeautifulSoup
import requests
import time
import re

from Aux import Aux

import sys
sys.path.append('/home/florian/anaconda3/lib/python3.7/site-packages')

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Crawler():

    Aux = Aux()

    def crawlData(self, WebUrl, rewUrl):

        # soup get rewards
        try:

            request_Rew = requests.get(rewUrl)
            doc = BeautifulSoup(request_Rew.text, 'html.parser')

            numOfRewards = 0
            for card in doc.select('.hover-group'):
                numOfRewards = numOfRewards + 1

            # selenium scroll page

            browser = webdriver.Chrome('./ChromeDriver/chromedriver')
            browser.get(WebUrl)

            time.sleep(1)

            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # number of pictures

            project_image = browser.find_elements_by_css_selector('[alt*="Project image"]')
            feature_image = browser.find_elements_by_class_name('js-feature-image ')
            post_elems = browser.find_elements_by_xpath("//figure/img")
            allImages = project_image + post_elems + feature_image

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
            if len(paragraphs) > 0:
                for paragraph in paragraphs:
                    text = str(paragraph.text)
                    text_Length = text_Length + len(text)
                    texts.append(text)

            # experience

            experience = 0

            # facebook friends
            hasFacebook = False
            numOfFbFriends = 0

            creator_Link = browser.find_elements_by_xpath("//div[@class='creator-name']//a")

            if len(creator_Link) > 0:

                linkToCreator = creator_Link[0].get_attribute("href")
                request_Creator = requests.get(linkToCreator)
                CreatorSoup = BeautifulSoup(request_Creator.text, 'html.parser')

                fbFriends = CreatorSoup.findAll('a', text=re.compile('friends'))
                if len(fbFriends) > 0:
                    hasFacebook = True
                    numInText = self.Aux.stringifyText(fbFriends[0])
                    numOfFbFriends = numInText

                experienceText = CreatorSoup.findAll('a', text=re.compile('created'))
                if len(experienceText) > 0:
                    numInText = self.Aux.stringifyText(experienceText[0])
                    experience = numInText

            else:
                beginner = browser.find_elements_by_xpath("//div[contains(text(), 'First created')]")

                if len(beginner) == 0:

                    expText = browser.find_elements_by_xpath("//div[contains(text(), 'created')]")
                    if len(expText) > 0:
                        numInText = self.Aux.stringifyText(expText)
                        experience = numInText

                creator_button = browser.find_elements_by_xpath("//div[@id='experimental-creator-bio']/button")
                if len(creator_button) > 0:
                    creator_button[0].click()
                    links = browser.find_elements_by_link_text('Facebook.com')
                    if len(links) == 0:
                        links = browser.find_elements_by_link_text('facebook.com')

                    if len(links) > 0:
                        hasFacebook = True
                        for link in links:
                            fbLink = link.get_attribute("href")
                        request_FB = requests.get(fbLink)
                        fbSoup = BeautifulSoup(request_FB.text, 'html.parser')
                        classAbo = fbSoup.findAll('div', text=re.compile('haben das abonniert'))
                        if len(classAbo) > 0:
                            numInText = self.Aux.stringifyText(classAbo[1])
                        else:
                            numInText = 0
                        numOfFbFriends = numInText
        except Exception as E:
            numOfImages, numOfRewards, hasVideo, texts, text_Length, hasFacebook, numOfFbFriends, experience = (0,) * 8
            print('data not crawlable' + str(E))

        return numOfImages, numOfRewards, hasVideo, texts, text_Length, hasFacebook, numOfFbFriends, experience
