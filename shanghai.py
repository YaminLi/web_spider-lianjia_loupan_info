import urllib.request
import re
import pandas as pd
import random
import time


hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},\
    {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},\
    {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},\
    {'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},\
    {'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}]

# cities = ['bj', 'cd', 'cq', 'cs', 'dl', 'dg', 'fs','gz','hz','hui','hk','jn','jx','lin','nj', 'nt','qd','sz','sjz','sy','tj','ts','ty','wh','wx','wf','wz','xa','xm','xz','yt','yz','zs','zh']

# shanghai suzhou
# raw_data={'城市':'t_city', '小区名':'t_name', '地址':'t_addr', '住宅类型':'t_type','均价':'t_avgCost'}
# df = pd.DataFrame(raw_data, columns=['城市', '小区名','地址', '住宅类型','均价'],index=[0])
df=pd.DataFrame()

url = 'http://sh.fang.lianjia.com/'
req = urllib.request.Request(url, headers=hds[random.randint(0,len(hds)-1)])
html = urllib.request.urlopen(req).read()
rPage =  re.compile(r' page-data="{&quot;totalPage&quot;:(.+?),&quot;curPage&quot;:1}">')
print(rPage.findall(html.decode('utf-8')))
pageNum = int(rPage.findall(html.decode('utf-8'))[0])
r = re.compile(r'href="/detail/.+">([^<].+?)</a>')
r1 = re.compile(r'</span>】(.+?)</span>')
r2 = re.compile(r'<span class="num">(.+?)</span>')
r3 = re.compile(r'<span class="normal-house">\n<span>(.+?)</span>\n</span>', re.M)


lpList = []
addrList =[]
avgCostList = []
# liveStyleList= []
for i in range(pageNum):
	if i==0:
		print(len(html))
		lpName=r.findall(html.decode('utf-8'))
		addr=r1.findall(html.decode('utf-8'))
		avgCost=r2.findall(html.decode('utf-8'))
		liveStyle = r3.findall(html.decode('utf-8'))
		length = min(len(lpName), len(addr), len(avgCost))
		lpList.extend(lpName[0:length])
		addrList.extend(addr[0:length])
		avgCostList.extend(avgCost[0:length])
		# liveStyleList.extend(liveStyle[0:length])
		for j in range(length):
			print(lpName[j])
			print(addr[j])
			print(avgCost[j])
			print(liveStyle[j])
	else:
		# print(i)
		html_tmp = ''
		req = urllib.request.Request(url+'list/pg'+str(i+1), headers=hds[random.randint(0,len(hds)-1)])
		html_tmp = urllib.request.urlopen(req).read()
		print(len(html_tmp))
		lpName=r.findall(html_tmp.decode('utf-8'))
		addr=r1.findall(html_tmp.decode('utf-8'))
		avgCost=r2.findall(html_tmp.decode('utf-8'))
		# liveStyle = r3.findall(html_tmp.decode('utf-8'))
		length = min(len(lpName), len(addr), len(avgCost))
		lpList.extend(lpName[0:length])
		addrList.extend(addr[0:length])
		avgCostList.extend(avgCost[0:length])
		# liveStyleList.extend(liveStyle[0:length])
		for j in range(length):
			print(lpName[j])
			print(addr[j])
			print(avgCost[j])
			# print(liveStyle[j])
# print(lpList)
# raw_data={'城市':cities[k], '小区名':lpList, '地址':addrList, '住宅类型':liveStyleList,'均价':avgCostList}
# df_tmp = pd.DataFrame(raw_data, columns=['城市', '小区名','地址', '住宅类型','均价'])
# # print(df)
# # print(df_tmp)
# df = df.append(df_tmp, ignore_index=True)
# # print(df)
# except IndexError:
# print('city name is', cities[k])

# # df = pd.DataFrame(raw_data, columns=['城市', '小区名','地址', '住宅类型','均价'])
# df.to_csv('lianjia.csv')