import scrapy
from scrapy_splash import SplashRequest

class blumeVC_spider(scrapy.Spider):

	name = 'blumeVC'
	start_url = ['http://blume.vc/portfolio-new/']
	
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
		for startup in response.xpath('/html/body/div[3]/div/div/div/div/div/div[4]/div/div/div/div/div[1]/div/article'):
			final_data = {}
			
			final_data['Startup Name'] = startup.xpath('./div[2]/h5/a/text()').extract_first()
			final_data['Startup URL'] = startup.xpath('./div[2]/h5/a/@href').extract_first()
			final_data['Logo URL'] = startup.xpath('./div[1]/div[3]/span/img/@src').extract_first()
			
			yield final_data