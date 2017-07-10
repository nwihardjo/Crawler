import scrapy
from scrapy_splash import SplashRequest
import csv
def clean_string(name):
	"""
	remove non-alphanumeric characters in the 'name' string to give the data to domain name
		args name: string going to be cleaned
	"""
	nameList = list(name)
	while nameList[0].isalnum() == False:
		nameList.remove(nameList[0])
	while nameList[-1].isalnum() == False:
		nameList.remove(nameList[-1])
	for char in nameList:
		if char.isalnum() == False:
			char = '-'

	return ''.join(nameList)

def generate_url(name):
	"""
	generate the url from each startup name based on its database / domain
		args name : startup name
	"""

	for char in name:
		if char.isalnum() == False:
			name = clean_string(name)
			break

	return ('http://e27.co/startup/' + name)

def generate_startup_list():
	"""
	read and list the list of startups which the data needs to be scraped
	"""
	info = 'Input the csv\'s filename and the filetype (ex: excelworkbook.csv) : '
	fileName = input(info)
	startupList = []
	with open(fileName, newline = '') as f:
		reader = csv.reader(f, delimiter = ',')
		skip = True
		for row in reader:
			if skip: 			#to skip the header
				skip = False
				contiue
			startupList.append(generate_url(row[7].lower()))

	return startupList

class e27_spider(scrapy.Spider):
	name = 'tia'
	start_urls = ['https://angel.co/flipkart']
	def start_requests(self):
		"""
		the function make a request for each url in the start_urls list
		fetch the requested url, and pass it to the callback, which is parse function
		"""
		for url in self.start_urls:
			yield SplashRequest(url = url, callback = self.parse, args={'http_method': 'GET','follow_redirects':False})
			# yield scrapy.Request(url, self.parse, meta={'splash':{'args':{'html':1, 'png':1,'dont_process_response':True}},'handle_httpstatus_list':[302],'dont_redirect':True})
	def parse(self, response):
		"""
		response: the fetched request received from start_requests
		the function return a dictionary (set of data) that contains the profile of the startup
		"""
		filename = 'asdf.html' # response.xpath('//*[@id="page-container"]/div[3]/div/div/div/div/div/div[2]/div[1]/div/h1/text()').extract_first()
		with open(filename, 'wb') as f:
			f.write(response.body)

		# final_data = {}
		# startup_name = response.xpath('//*[@id="page-container"]/div[3]/div/div/div/div/div/div[2]/div[1]/div/h1/text()').extract_first()
		# startup_founding_date = response.xpath('//*[@id="page-container"]/div[3]/div/div/div/div/div/div[2]/div[1]/div/p[3]/span/text()').extract_first()
		# startup_description = response.xpath('//*[@id="page-container"]/div[4]/div/div/div/div/div[1]/div[1]/div[1]/div/p/text()').extract_first()

		# final_data['Name'] = startup_name
		# final_data['Founding Date'] = startup_founding_date
		# final_data['Description'] = startup_description
		# print (final_data)
		
		# startup_funding = response.selector.xpath('//*[@id="funding_table"]')
		# for fund in startup_funding.css('.table-col'):
		# 	print(fund.xpath('/div[1]/div/div[2]/div/text()').extract_first())

	
		# for fund in startup_funding.css('div.table-col'):
		# 	x = fund.css('div.comp-name data-col')
		# 	y = x.css('div.startup-container')
		# 	z = y.css('div.name')
		# 	a = z.css('a.item-label bold::text')
		# 	print(a)

		# filename = 'scraped_data.csv'

		# with open(filename, 'wb') as f:
		# 	ff = ['Name','Founding Date','Description']
		# 	wr = csv.DictWriter(f, fieldnames = ff)
		# 	wr.writeheader()
		# 	wr.writerow({'Name': startup_name,'Founding Date': startup_founding_date,'Description': startup_description})
		# print (final_data)
