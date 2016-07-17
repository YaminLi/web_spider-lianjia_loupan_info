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

url = 'http://su.lianjia.com/xiaoqu/'
# req = urllib.request.Request(url, headers=hds[random.randint(0,len(hds)-1)])
html = urllib.request.urlopen(url).read()
print(len(html))
rPage =  re.compile(r'<a href="/xiaoqu/d100" gahref="results_totalpage">(.+?)</a>')
print(rPage.findall(html.decode('utf-8')))
pageNum = int(rPage.findall(html.decode('utf-8'))[0])
r = re.compile(r'<a name="selectDetail".+">([^<].+?)</a>')
r1 = re.compile(r'districtName="(.+?)"\splateName="(.+?)"')
r2 = re.compile(r'<span class="num">(.+?)\r\n\s+?\r\n\t+?<img src')
# r3 = re.compile(r'<span class="normal-house">\r\n\s+?<span>(.+?)</span>\r\n\s+?</span>\r\n')


lpList = []
addrList =[]
avgCostList = []
liveStyleList= []
for i in range(pageNum):
	if i==0:
		print(len(html))
		lpName=r.findall(html.decode('utf-8'))
		# print(lpName)
		addr_tmp=r1.findall(html.decode('utf-8'))
		addr = []
		for x in range(len(addr_tmp)):
			addr.append(addr_tmp[x][0]+addr_tmp[x][1])
		# print(addr)
		avgCost=r2.findall(html.decode('utf-8'))
		# print(avgCost)
		# liveStyle = r3.findall(html.decode('utf-8'))
		length = min(len(lpName), len(addr), len(avgCost))
		lpList.extend(lpName[0:length])
		addrList.extend(addr[0:length])
		avgCostList.extend(avgCost[0:length])
		# liveStyleList.extend(liveStyle[0:length])
		# for j in range(length):
		# 	print(lpName[j])
		# 	print(addr[j])
		# 	print(avgCost[j])
		# 	print(liveStyle[j])
	else:
	# 	# print(i)
		html_tmp = ''
		url_tmp = url+'d'+str(i+1)
		# req = urllib.request.Request(url_tmp, headers=hds[random.randint(0,len(hds)-1)])
		html_tmp = urllib.request.urlopen(url_tmp).read()
	# 	print(len(html_tmp))
		lpName=r.findall(html_tmp.decode('utf-8'))
	# 	addr=r1.findall(html_tmp.decode('utf-8'))
		addr_tmp=r1.findall(html.decode('utf-8'))
		addr = []
		for x in range(len(addr_tmp)):
			addr.append(addr_tmp[x][0]+addr_tmp[x][1])
		avgCost=r2.findall(html_tmp.decode('utf-8'))
	# 	liveStyle = r3.findall(html_tmp.decode('utf-8'))
		length = min(len(lpName), len(addr), len(avgCost))
		lpList.extend(lpName[0:length])
		addrList.extend(addr[0:length])
		avgCostList.extend(avgCost[0:length])
	# 	liveStyleList.extend(liveStyle[0:length])
		# for j in range(length):
		# 	print(lpName[j])
		# 	print(addr[j])
		# 	print(avgCost[j])
		# 	print(liveStyle[j])
# print(lpList)
raw_data={'城市':'su', '小区名':lpList, '地址':addrList, '住宅类型':'','均价':avgCostList}
df = pd.DataFrame(raw_data, columns=['城市', '小区名','地址', '住宅类型','均价'])

df.to_csv('./quanguo/suzhou.csv')

