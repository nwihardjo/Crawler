import scrapy
from scrapy_splash import SplashRequest

class helion_spider(scrapy.Spider):

	name = 'helion'
	start_url = ['http://www.helionvc.com/portfolio.html']
	base_url = 'http://www.helionvc.com/'
	
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
		for startup in response.xpath('//*[@id="isotope-container"]/div'):
			final_data = {}
			final_data['Startup Name'] = startup.xpath('./div/div[3]/div/h5/span/text()').extract_first()
			final_data['Startup URL'] = startup.xpath('./div/div[2]/div/a/@href').extract_first()
			
			if startup.xpath('./div/div[2]/div/a/img/@src').extract_first() is not None:
				final_data['Logo URL'] = self.base_url + startup.xpath('./div/div[2]/div/a/img/@src').extract_first()
			else: final_data['Logo URL'] = None
			
			final_data['Industry'] = startup.xpath('./div/div[1]/div/text()').extract_first()

			yield final_data