import sys
import requests
client = requests.session()

login_url = 'https://www.cuemath.com/admin/login/?next=/admin/'

client = requests.session()
client.get(login_url)

csrftoken = client.cookies['csrftoken']
login_data = dict(username='rahul', password='cuemath4life', csrfmiddlewaretoken=csrftoken, next='/admin/')
r = client.post(login_url, data=login_data, headers=dict(Referer=login_url))
print(r.text)

cityAnalyticsUrl = 'https://www.cuemath.com/admin/analytics/cityanalytics/'
p = client.get(cityAnalyticsUrl, headers = dict(Referer=login_url))
cityAnalyticsExportUrl = 'https://www.cuemath.com/admin/analytics/cityanalytics/export/?'
q = client.get(cityAnalyticsExportUrl)
csrftoken = client.cookies['csrftoken']

export_data = dict(file_format=0, csrfmiddlewaretoken=csrftoken, next='/')
t = client.post(cityAnalyticsExportUrl, data=export_data, headers=dict(Referer=cityAnalyticsExportUrl))
g = t.text.split('\n')
csvfile = open('../CueMath/CueLearn/Data/pythonexport.csv', 'w')
csvfile.write( t.text.replace("\r\n","\n") )
csvfile.close()