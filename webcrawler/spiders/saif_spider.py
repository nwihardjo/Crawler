import scrapy
from scrapy_splash import SplashRequest

class saif_spider(scrapy.Spider):

	name = 'saif'
	start_url = ['http://www.saifpartners.com/portfolio/']
	
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
		for startup in response.xpath('//*[@id="contact__main"]/div[2]/section[3]/div/div/a'):
			yield SplashRequest(url = startup.xpath('./@href').extract_first(), callback = self.parse_startup)

	def parse_startup(self, response):
		final_data = {}
		final_data['Startup Name'] = ' '.join(response.url.split('/')[-2].split('-'))
		final_data['Startup URL'] = response.xpath('//*[@id="bank__main"]/section/div/div[2]/div/ul/li[1]/a/@href').extract_first()
		final_data['Logo URL'] = response.xpath('//*[@id="bank__main"]/section/div/div[1]/img[1]/@src').extract_first()
		final_data['Facebook URL'] = response.xpath('//*[@id="bank__main"]/section/div/div[2]/div/ul/li[2]/a/@href').extract_first()
		final_data['Twitter URL'] = response.xpath('//*[@id="bank__main"]/section/div/div[2]/div/ul/li[3]/a/@href').extract_first()
		final_data['Description'] = response.xpath('//*[@id="bank__main"]/section/div/div[1]/div[1]/text()').extract_first()
		final_data['Industry'] = response.xpath('//*[@id="bank__main"]/section/div/div[1]/h1/text()').extract_first().lstrip().rstrip()

		yield final_data