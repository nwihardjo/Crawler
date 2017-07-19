
import json
import requests

response = requests.get('https://www.accel.com/fetchrapi/companies?returnMeta=true')

if not response.status_code == 200:
	print("API'S STATUS CODE IS NOT 200. CHECK THE RELATED PROGRAMME")
	quit()

data = response.json()
print('NUMBER OF STARTUP:', len(data['data']['data']['objects']))