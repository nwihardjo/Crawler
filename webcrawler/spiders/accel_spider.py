import json
import requests
import csv

def input(data, field, library, key):
	try: library[key] = startup[field]
	except: library[key] = None
	return library

response = requests.get('https://www.accel.com/fetchrapi/companies?returnMeta=true')

if not response.status_code == 200:
	print("API'S STATUS CODE IS NOT 200. CHECK THE RELATED PROGRAMME")
	quit()

data = response.json()
print('NUMBER OF STARTUP:', len(data['data']['data']['objects']))

count = 0
final_data = []
for startup in data['data']['data']['objects']:
	try:
		"""
		parse and extract startups solely based in India
		"""
		if startup['regions'][0]['name'] == 'India':
			startup_data = {}
			input(startup, 'name',startup_data, 'Startup Name')
			input(startup, 'externalLink', startup_data, 'Startup URL')
			input(startup, 'description', startup_data, 'Description')
			input(startup, 'investmentYear', startup_data, 'Invested Year')
			input(startup, 'investmentSeries', startup_data, 'Investment Series')
			input(startup, 'exited', startup_data, 'Exit by Accel Partners')
			
			"""
			Industries field is not looping through every categories
			"""
			for categories in startup['categories']:
				startup_data['Industry'] = []
				startup_data['Industry'].append(categories['name'])
			
			print(startup['categories'])

			final_data.append(startup_data)
	except:
		continue

with open('accel.csv','w') as f:
	fieldnames = ['Startup Name','Startup URL','Description','Invested Year','Invested Year','Investment Series','Exit by Accel Partners','Industry']
	writer = csv.DictWriter(f, fieldnames = fieldnames)
	writer.writeheader()
	for startup in final_data:
		writer.writerow(startup)