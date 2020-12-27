from hashlib import new
from django.http import response
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from googletrans.client import Translator
import requests
import re
from .gooleapi import Googleapi

class Crawlers(ABC):
 
    def __init__(self, translated_lang, translated_result):
        self.translated_lang = translated_lang
        self.translated_result = translated_result 
        self.result = []
 
    @abstractmethod
    def crawl(self):
        pass

class Crawler(Crawlers):

    def replace_non_chinese(self, sentence):
        filtrate = re.compile(u'[^\u4E00-\u9FA50-9]') # non-Chinese unicode range
        new_sentence = filtrate.sub(r'', sentence) # remove all non-Chinese characters
        return new_sentence

    def replace_non_alphanumeric(self, sentence):
        filtrate = re.compile('[^0-9a-zA-Z]')
        new_sentence = filtrate.sub(' ', sentence)
        return new_sentence

    def crawl(self):
        if self.translated_lang == "zh":
            url = "https://tw.ichacha.net/" + self.translated_result + ".html"
            print("find zh ex : ", url)
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            try:
                sentence_tag = soup.find(
                    "div", {"id":"sent_dt1"}
                )
                sentences = sentence_tag.findAll(
                    "li"
                )
                for sentence in sentences[:-1]:
                    sentence = sentence.getText()
                    sentence = self.replace_non_chinese(sentence)
                    sentence = re.sub('\s+', ' ', sentence)
                    sentence += "。"
                    
                    translator = Translator()
                    sentence = translator.translate(sentence, 'zh-TW').text
                    self.result.append(sentence)
            except: return []

        elif self.translated_lang == "en":
            url = "https://tw.ichacha.net/" + self.translated_result + ".html"
            print("find en ex : ", self.translated_result, url)
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            try:
                sentence_tag = soup.find(
                    "div", {"id":"sent_dt1"}
                )
                sentences = sentence_tag.findAll(
                    "li"
                )
                for sentence in sentences[:-1]:
                    sentence = sentence.getText()
                    sentence = self.replace_non_alphanumeric(sentence)
                    sentence = re.sub('\s+', ' ', sentence)
                    sentence += "."
                    self.result.append(sentence)
            except: return []

        elif self.translated_lang == "ja":
            url = "https://tw.ichacha.net/jp/" + self.translated_result + ".html"
            print("find ja ex", url)
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            try:
                sentence_tag = soup.find(
                    "div", {"id":"sent_dt1"}
                )
                sentences = sentence_tag.findAll(
                    "li"
                )
                for sentence in sentences[:-1]:
                    sentence = sentence.getText()
                    sentence = sentence.split("．")[0]
                    sentence = re.sub('\s+', ' ', sentence)
                    self.result.append(sentence)
            except: return []

        return self.result
