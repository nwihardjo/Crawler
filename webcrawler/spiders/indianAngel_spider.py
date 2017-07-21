import scrapy
from scrapy_splash import SplashRequest
import requests
from bs4 import BeautifulSoup

class indianAngel_spider(scrapy.Spider):

	name = 'indianAngel'
	start_url = ['https://www.indianangelnetwork.com/portfolios']
	base_url = 'http://www.indianangelnetwork.com'
	
	def start_requests(self):
		"""
			the function make a request for each url in the start_urls list
			fetch the requested url, and pass it to the callback, which is parse function
		"""
		for url in self.start_url:
			yield SplashRequest(url = url, callback = self.parse)

	def parse(self, response):
		"""
			response: the fetched request received from start_requests
			the function return a dictionary (set of data) that contains the profile of the startup
		"""
		for category in response.xpath('/html/body/section/div/div/div/div[1]/ul/li'):
			yield SplashRequest(url = self.base_url + category.xpath('./figure/a/@data-id').extract_first(), callback = self.parse_category)

	def parse_category(self, response):
		for startup in response.xpath('/html/body/div/div[2]/div'):
			final_data = {}

			startup_profile = requests.get(self.base_url + startup.xpath('./a/@url').extract_first())
			soup = BeautifulSoup(startup_profile.text, 'html.parser')

			final_data['Startup Name'] = soup.find('span', class_ = 'company-name').find('strong').get_text()
			final_data['Startup URL'] = soup.find('a', class_ = 'website-address').get_text()
			final_data['Logo URL'] = soup.find('img', attrs = {'title': 'Portfolio Logo'})['src']

			if soup.find('a', class_ = 'facebook') is not None:	final_data['Facebook URL'] = soup.find('a', class_ = 'facebook')['href']
			else: final_data['Facebook URL'] = None
			if soup.find('a', class_ = 'linkedin') is not None:	final_data['LinkedIn URL'] = soup.find('a', class_ = 'linkedin')['href']
			else: final_data['LinkedIn URL'] = None
			
			final_data['Description'] = soup.find('p', class_ = 'mb-20').get_text()
			final_data['Industry'] = response.xpath('/html/body/div/div[1]/div/h3/text()').extract_first()

			yield final_data