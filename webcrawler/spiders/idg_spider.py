import scrapy
from scrapy_splash import SplashRequest

class idg_spider(scrapy.Spider):

	name = 'idg'
	start_url = ['http://www.idgvcindia.com/idg_india_portfolio.html']
	base_url = 'http://www.idgvcindia.com/'
	
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
		for startup in response.xpath('//*[@id="projects"]/div[1]/div[2]/div'):
			final_data = {}
			name_list = startup.xpath('./div/a/img/@src').extract_first().split('_')
			name_list[-1] = name_list[-1].split('.')[0]
			final_data['Startup Name'] = ' '.join(name_list[1:])
			final_data['Startup URL'] = startup.xpath('./div/a/@href').extract_first()
			final_data['Logo URL'] = self.base_url + startup.xpath('./div/a/img/@src').extract_first()
			
			yield final_data
