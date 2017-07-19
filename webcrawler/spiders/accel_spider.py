from pprint import pprint
import json
import requests

response = requests.get('https://www.accel.com/fetchrapi/companies?returnMeta=true')

if not response.status_code == 200:
	print("API'S STATUS CODE IS NOT 200. CHECK THE RELATED PROGRAMME")
	quit()

data = response.json()
print('NUMBER OF STARTUP:', len(data['data']['data']['objects']))

count = 0
for startup in data['data']['data']['objects']:
	try:
		if startup['regions'][0]['name'] == 'India':
			final_data = {}
			try: final_data['Startup Name'] = startup['name']
			except:
	except:
		continue
