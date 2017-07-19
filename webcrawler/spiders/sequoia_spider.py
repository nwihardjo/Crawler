import scrapy
from scrapy_splash import SplashRequest
import requests
from bs4 import BeautifulSoup
import re

class sequoia_spider(scrapy.Spider):

	name = 'sequoia'
	start_url = ['https://www.sequoiacap.com/india/companies/']

	def start_requests(self):
		"""
			the function make a request for each url in the start_urls list
			fetch the requested url, and pass it to the callback, which is parse function
		"""
		for url in self.start_url:
			yield SplashRequest(url = url, callback = self.parse)

	def parse(self, response):
		for startup in response.xpath('//*[@id="allColumn"]/div/li'):
			startup_url = 'https://www.sequoiacap.com' + startup.xpath('./div/@data-partial').extract_first()
			print('DEBUG: GETTING STARTUP PROFILE: ', startup_url)

			r = requests.get(startup_url)
			soup = BeautifulSoup(r.text, 'html.parser')

			final_data = {}
			final_data['Startup Name'] = soup.find('div', class_ = '_title -large-title js-panel-name').get_text().lstrip().rstrip()

			links = soup.find_all('a',class_ = 'social-link')
			for link in soup.find_all('a', class_ = 'social-link'):
				if 'Website' in link['onclick']:
					final_data['Startup URL'] = link['href']
				elif 'Twitter' in link['onclick']:
					final_data['Twitter URL'] = link['href']
				elif 'LinkedIn' in link['onclick']:
					final_data['LinkedIn URL'] = link['href']

			final_data['Logo URL'] = soup.find('div', class_ = 'company-holder _logo').find('img')['src']
			try:
				final_data['Description'] = soup.find('div',class_ = 'company-holder _body-copy -grey-dark').find('p').get_text()
			except:
				final_data['Description'] = None
			final_data['Founding Year'] = re.sub('[^0-9]','',soup.find('span', class_ = '-body-copy -grey-light -block').get_text())
			final_data['Invested Year'] = re.sub('[^0-9]','',soup.find('li', class_ = '-body-copy -grey-light js-person-name').get_text())

			yield final_data
