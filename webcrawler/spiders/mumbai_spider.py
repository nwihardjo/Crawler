import scrapy
from scrapy_splash import SplashRequest

class mumbai_spider(scrapy.Spider):

	name = 'mumbai'
	start_url = ['http://www.mumbaiangels.com/ma_portfolio_view_all.php']
	base_url = 'http://www.mumbaiangels.com/'

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
		print('DEBUG: NOW AT PAGE: ', response.xpath('//*[@id="maincontent"]/table/tbody/tr[9]/td/table/tbody/tr/td[3]/span/strong').extract_first())
		
		indexLevel1 = 0
		for row in response.xpath('//*[@id="maincontent"]/table/tbody/tr'):
			indexLevel1 += 1
			if indexLevel1 == 1 or indexLevel1 % 2 == 0 or indexLevel1 == 9:
				continue

			indexLevel2 = 0
			for startup in row.xpath('./td'):
				indexLevel2 += 1
				if indexLevel2 % 2 == 0:
					continue
								
				if startup.xpath('./a/@href').extract_first() is not None:
					start_url = self.base_url + startup.xpath('./a/@href').extract_first()
					yield SplashRequest(url = start_url, callback = self.parse_startup)

		###		Follow the next page	###
		if response.xpath('//*[@id="maincontent"]/table/tbody/tr[9]/td/table/tbody/tr/td[5]/a/@href').extract_first() is not None:
			yield SplashRequest(url = self.base_url + response.xpath('//*[@id="maincontent"]/table/tbody/tr[9]/td/table/tbody/tr/td[5]/a/@href').extract_first(), callback = self.parse)


	def parse_startup(self, response):
		final_data = {}
		name_list = response.url.split('_')
		name_list[-1] = name_list[-1].split('.')[0]
		final_data['Startup Name'] = ' '.join(name_list[3:])

		print('DEBUG: PARSING:', final_data['Startup Name'])

		final_data['Startup URL'] = response.xpath('//*[@id="maincontent"]/table/tbody/tr[4]/td/p[3]/a/@href').extract_first()
		
		if response.xpath('//*[@id="maincontent"]/table/tbody/tr[3]/td/p/a/img/@src').extract_first() is not None:
			final_data['Logo URL'] = self.base_url + response.xpath('//*[@id="maincontent"]/table/tbody/tr[3]/td/p/a/img/@src').extract_first()
		elif response.xpath('//*[@id="maincontent"]/table/tbody/tr[3]/td/p/img/@src').extract_first() is not None:
			final_data['Logo URL'] = self.base_url + response.xpath('//*[@id="maincontent"]/table/tbody/tr[3]/td/p/img/@src').extract_first()


		final_data['Description'] = response.xpath('//*[@id="maincontent"]/table/tbody/tr[4]/td/p[1]/text()').extract_first()
		final_data['Industry'] = response.xpath('//*[@id="maincontent"]/table/tbody/tr[2]/td/span/text()').extract_first()

		yield final_data