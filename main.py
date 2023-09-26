import requests
import xmltodict
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
import matplotlib.font_manager as fm
from matplotlib import rc
from sklearn.linear_model import LinearRegression
import os

rc('font', family='NanumGothic')

url = 'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev'
DECODED_SERVICE_KEY = os.getenv('DECODED_SERVICE_KEY')
params = {
    'serviceKey': DECODED_SERVICE_KEY,
    #'pageNo': '1',
    #'numOfRows': '100',
    'LAWD_CD': '11410',
    'DEAL_YMD': '202011',
}
response = requests.get(url, params=params)
response_dict = xmltodict.parse(response.content)
print(response_dict)
items = response_dict['response']['body']['items']['item']
df = pd.DataFrame(items)

df['거래금액'] = df['거래금액'].str.replace(',', '').astype(float)
df['전용면적'] = df['전용면적'].astype(float)

X = df[['전용면적']]/3.3
y = df['거래금액']

# Create a linear regression model
model = LinearRegression()
model.fit(X, y)

# Get the model's coefficients
slope = model.coef_[0]
intercept = model.intercept_

# Plot the regression line and the original data
plt.figure(figsize=(10, 6))
plt.scatter(X, y, label="Original Data", alpha=0.5)
plt.plot(X, model.predict(X), color='r', label="Regression Line")
plt.xlabel('Area (전용면적(평))')
plt.ylabel('Transaction Amount (거래금액(만원)')
plt.legend()
plt.title('Linear Regression: Transaction Amount vs Area')

# Add the equation to the plot
equation = f'y = {slope:.2f}x + {intercept:.2f}'
plt.text(30, 20000, equation, fontsize=12, color='red', bbox=dict(facecolor='white', edgecolor='white', pad=5))

# Save the plot as a PNG file
plt.savefig('seodaemon_linear_regression_plot.png', dpi=300, bbox_inches='tight')