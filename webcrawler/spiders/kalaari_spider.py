import scrapy
from scrapy_splash import SplashRequest

class kalaari_spider(scrapy.Spider):

	name = 'kalaari'
	start_url = ['http://www.kalaari.com/portfolio']
	
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
		for startup in response.xpath('//*[@id="menu1"]/ul/li'):
			final_data = {}
			final_data['Startup Name'] = startup.xpath('./a/div/p/text()').extract_first()
			final_data['Startup URL'] = startup.xpath('./a/@href').extract_first()
			final_data['Logo URL'] = startup.xpath('./a/img/@src').extract_first()

			yield final_data
