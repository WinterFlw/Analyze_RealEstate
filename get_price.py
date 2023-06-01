import requests
import xmltodict
import pandas as pd
import os

url = 'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev'

DECODED_SERVICE_KEY = os.getenv('DECODED_SERVICE_KEY')
params = {
    'serviceKey': DECODED_SERVICE_KEY,
    'pageNo': '1',
    'numOfRows': '10',
    'LAWD_CD': '11110',
    'DEAL_YMD': '201512',
}

response = requests.get(url, params=params)

# Convert the XML response to a Python dictionary
response_dict = xmltodict.parse(response.content)

# Extract the item list from the response
items = response_dict['response']['body']['items']['item']

# Convert the item list to a pandas DataFrame
df = pd.DataFrame(items)

print(df.head()