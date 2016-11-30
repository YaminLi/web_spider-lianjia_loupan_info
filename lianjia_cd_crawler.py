import re
import requests
import json
import pandas as pd
import urllib.request
import random
import os
import sys


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

def login(username, password):
    s = requests.session()

    home_url = 'http://bj.lianjia.com/'
    auth_url = 'https://passport.lianjia.com/cas/login?service=http%3A%2F%2Fbj.lianjia.com%2F'

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'passport.lianjia.com',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
    }

    s.get(home_url)
    res = s.get(auth_url, headers=headers)
    # print(res.content)
    # print(res.headers)

    # r=re.compile(r'Set-Cookie: JSESSIONID=(.+?);')
    set_cookie = res.headers['Set-Cookie']
    idx = set_cookie.find(';')
    jsesseionid = set_cookie[11:idx]
    # print(jsesseionid)

    pattern = re.compile(r'value=\"(LT-.+?)\"')
    lt = pattern.findall(res.content.decode('utf-8'))[0]
    # print(lt)

    pattern = re.compile(r'name="execution" value="(.+?)"')
    execution = pattern.findall(res.content.decode('utf-8'))[0]
    # print(execution)

    data = {
        'username': 'username',
        'password': 'password',
        'execution': execution,
        '_eventId': 'submit',
        'lt': lt,
        'verifyCode': '',
        'redirect': '',
    }

    res=s.post(auth_url, data)
    print(res)

    return s

def getDistrictName(username, password):
    s=login(username, password)
    chengjiao_url = 'http://cd.lianjia.com/chengjiao/'
    res = s.get(chengjiao_url)
    # print(res.headers)
    content = res.content.decode('utf-8')
    # # print(content)
    pattern = re.compile(r'</a><a href="(.+?)" title="成交房成都([^0-9一二三].+?)">')
    # print(pattern.findall(content))
    links = []
    district = []
    for i in range(len(pattern.findall(content))):
      links.append(pattern.findall(content)[i][0])
      district.append(pattern.findall(content)[i][1])
      # print(pattern.findall(content)[i])
    # print(links)
    # print(district)
    for i in range(len(links)):
        # print(links[i])
        if links[i] == '/chengjiao/xindou/':
            url = 'http://cd.lianjia.com'+links[i]
            res = s.get(url)
            content = res.content.decode('utf-8')
            pattern = re.compile(r'class="on">不限</a>(.+?)</div></dd></dl>')
            tmp = pattern.findall(content)[0]
            pattern = re.compile(r'<a href="/chengjiao/([^"].+?)">(.+?)</a>')
            sub_links = []
            sub_district = []
            for j in range(len(pattern.findall(tmp))):
                sub_links.append(pattern.findall(tmp)[j][0])
                sub_district.append(pattern.findall(tmp)[j][1])
            # print(sub_links)
            print(sub_district)
            path = '/Users/Michael/Documents/WebCrawler/lianjia/cd'
            # print(sys.path[0])
            new_path = os.path.join(path, district[i])
            print(new_path)
            if not os.path.isdir(new_path):
                os.makedirs(new_path)
            # for j in range(1):
            for j in range(len(sub_links)):
                # print(sub_links[j])
                url = 'http://cd.lianjia.com/chengjiao/'+sub_links[j]
                res = s.get(url)
                content = res.content.decode('utf-8')
                rPage =  re.compile(r'page-data=\'{"totalPage":(.+?),"curPage":')
                if rPage.findall(content):
                    total_page = int(rPage.findall(content)[0])
                    info = {'id':[], 'name':[], 'type':[], 'size':[], 'direction':[],'floor':[], 'year':[], 'signTime':[], 'signSource':[], 'unitPrice':[], 'unit':[], 'signPrice':[]}
                    ptn_get_xiaoqu_info = re.compile(r'<h2><a href="http://cd.lianjia.com/chengjiao/(.+?)\.html" target="_blank">(.+?)</a></h2><div><div class="col-1 fl"><div class="other"><div class="con">(.+?)</div></div><div class="introduce">')
                    ptn_get_deal_info = re.compile(r'<div class="dealType"><div class="fl"><div class="div-cun">(.+?)</div><p>(.+?)</p></div><div class="fl"><div class="div-cun">(.+?)<span>(.+?)</span></div><p>签约单价</p></div><div class="fr"><div class="div-cun">(.+?)<span>(.+?)</span>')
                    # for k in range(1):
                    for k in range(total_page):
                        url = 'http://cd.lianjia.com/chengjiao/'+sub_links[j]+'pg'+str(k+1)
                        res =  s.get(url)
                        content = res.content.decode('utf-8')
                        xiaoqu_info = ptn_get_xiaoqu_info.findall(content)
                        deal_info = ptn_get_deal_info.findall(content)
                        # for t in range(1):
                        for t in range(len(xiaoqu_info)):
                            info['id'].append(xiaoqu_info[t][0])

                            idx1 = xiaoqu_info[t][1].find(' ')
                            # print(xiaoqu_info[t][1][0:idx1])
                            info['name'].append(xiaoqu_info[t][1][0:idx1])
                            idx2 = xiaoqu_info[t][1].rfind(' ')
                            # print(xiaoqu_info[t][1][idx1+1:idx2])
                            # print(xiaoqu_info[t][1][idx2+1:])
                            info['type'].append(xiaoqu_info[t][1][idx1+1:idx2])
                            info['size'].append(xiaoqu_info[t][1][idx2+1:])

                            idx1 = xiaoqu_info[t][2].find('/')
                            # print(xiaoqu_info[t][2][0:idx1])
                            info['direction'].append(xiaoqu_info[t][2][0:idx1])
                            idx2 = xiaoqu_info[t][2].rfind('/')
                            # print(xiaoqu_info[t][2][idx1+1:idx2])
                            # print(xiaoqu_info[t][2][idx2+1:])
                            info['floor'].append(xiaoqu_info[t][2][idx1+1:idx2])
                            info['year'].append(xiaoqu_info[t][2][idx2+1:])

                            info['signTime'].append(deal_info[t][0])
                            info['signSource'].append(deal_info[t][1])
                            info['unitPrice'].append(deal_info[t][2])
                            info['unit'].append(deal_info[t][3])
                            info['signPrice'].append(deal_info[t][4])
                    raw_data={'id':info['id'], 'name':info['name'], 'type':info['type'], 'size':info['size'], 'direction':info['direction'], 'floor':info['floor'], 'year':info['year'],'signTime':info['signTime'], 'signSource':info['signSource'], 'unitPrice':info['unitPrice'], 'unit':info['unit'], 'signPrice':info['signPrice']}
                    df = pd.DataFrame(raw_data, columns=['id', 'name', 'type', 'size', 'direction', 'floor', 'year', 'signTime', 'signSource', 'unitPrice', 'unit', 'signPrice'])
                    df.to_csv('/Users/Michael/Documents/WebCrawler/lianjia/cd/'+district[i]+'/'+sub_district[j]+'.csv')

def getTransList():
    t=pd.read_csv('./quanguo1/xiaoqu/cd_id.csv', encoding='gbk')
    xiaoqu_id = t['xiaoqu_id']
    for k in range(len(xiaoqu_id)):
        try:
            url = 'http://cd.lianjia.com/chengjiao/getinfo/?page=1&id='+xiaoqu_id[k]+'&type=resblock&p=1'
            req = urllib.request.Request(url, headers=hds[random.randint(0,len(hds)-1)])
            html = urllib.request.urlopen(req).read()
            data = json.loads(html.decode('utf-8'))
            totalPage = int(data['totalPage'])
            print(totalPage)
            itemData = data['itemData']
            # info_title = ['schoolInfoString', 'houseArea', 'year', 'buildingType', 'houseUrl', 'otherSourceUnitPriceMin', 'soleString', \
            #             'unitPrice', 'fluctuation', 'resblockName', 'resblockID', 'otherSourcePriceMin', 'otherSourceUnitPriceMax', \
            #             'frameOrientation', 'isDisplay', 'floorInfo', 'listPicUrl', 'subTitle', 'signTime', 'subwayInfoString', \
            #             'finishYear', 'houseCode', 'signSourceText', 'signPrice', 'sameFrameUrl', 'signSource', 'hallNum', 'titleString', \
            #             'decorationType', 'signSourceId', 'roomNum', 'framePicUrl','picNum']
            # info = {'schoolInfoString':[], 'houseArea':[], 'year':[], 'buildingType':[], 'houseUrl':[], 'otherSourceUnitPriceMin':[], \
            #         'soleString':[], 'unitPrice':[], 'fluctuation':[], 'resblockName':[], 'resblockID':[], 'otherSourcePriceMin':[], \
            #         'otherSourceUnitPriceMax':[], 'frameOrientation':[], 'isDisplay':[], 'floorInfo':[], 'listPicUrl':[], 'subTitle':[], \
            #         'signTime':[], 'subwayInfoString':[], 'finishYear':[], 'houseCode':[], 'signSourceText':[], 'signPrice':[], 'sameFrameUrl':[], \
            #         'signSource':[], 'hallNum':[], 'titleString':[], 'decorationType':[], 'signSourceId':[], 'roomNum':[], 'framePicUrl':[],'picNum':[]}
            for i in range(len(itemData)):
                print(itemData[i]['resblockName'])
            #     for j in range(len(info_title)):
            #         info[info_title[j]].append(itemData[i][info_title[j]])

            # for x in range(totalPage-1):
            #     url = 'http://'+cities[k]+'.lianjia.com/chengjiao/getinfo/?page=1&id='+xiaoqu_id[k]+'&type=resblock&p='+str(x+2)
            #     req = urllib.request.Request(url, headers=hds[random.randint(0,len(hds)-1)])
            #     html = urllib.request.urlopen(req).read()
            #     data = json.loads(html.decode())
            #     itemData = data['itemData']
            #     for i in range(len(itemData)):
            #         for j in range(len(info_title)):
            #             info[info_title[j]].append(itemData[i][info_title[j]])

            # raw_data =  {'schoolInfoString':info['schoolInfoString'], 'houseArea':info['houseArea'], 'year':info['year'], 'buildingType':info['buildingType'],\
            #             'houseUrl':info['houseUrl'], 'otherSourceUnitPriceMin':info['otherSourceUnitPriceMin'], 'soleString':info['soleString'], 'unitPrice':info['unitPrice'], \
            #             'fluctuation':info['fluctuation'], 'resblockName':info['resblockName'], 'resblockID':info['resblockID'], 'otherSourcePriceMin':info['otherSourcePriceMin'],\
            #             'otherSourceUnitPriceMax':info['otherSourceUnitPriceMax'], 'frameOrientation':info['frameOrientation'], 'isDisplay':info['isDisplay'],\
            #             'floorInfo':info['floorInfo'], 'listPicUrl':info['listPicUrl'], 'subTitle':info['subTitle'], 'signTime':info['signTime'],\
            #             'subwayInfoString':info['subwayInfoString'], 'finishYear':info['finishYear'], 'houseCode':info['houseCode'], 'signSourceText':info['signSourceText'],\
            #             'signPrice':info['signPrice'], 'sameFrameUrl':info['sameFrameUrl'], 'signSource':info['signSource'], 'hallNum':info['hallNum'],\
            #             'titleString':info['titleString'], 'decorationType':info['decorationType'], 'signSourceId':info['signSourceId'], 'roomNum':info['roomNum'], \
            #             'framePicUrl':info['framePicUrl'],'picNum':info['picNum']}
            # df = pd.DataFrame(raw_data, columns=['schoolInfoString', 'houseArea', 'year', 'buildingType', 'houseUrl', 'otherSourceUnitPriceMin', 'soleString', \
            #             'unitPrice', 'fluctuation', 'resblockName', 'resblockID', 'otherSourcePriceMin', 'otherSourceUnitPriceMax', \
            #             'frameOrientation', 'isDisplay', 'floorInfo', 'listPicUrl', 'subTitle', 'signTime', 'subwayInfoString', \
            #             'finishYear', 'houseCode', 'signSourceText', 'signPrice', 'sameFrameUrl', 'signSource', 'hallNum', 'titleString', \
            #             'decorationType', 'signSourceId', 'roomNum', 'framePicUrl','picNum'])
            # df.to_csv('./quanguo1/chengjiao_list/cd/'+xiaoqu_id[k]+'.csv')
        except IndexError:
            print('city name is', cities[k])
        except json.decoder.JSONDecodeError:
            err_id.append(xiaoqu_id[k])


if __name__=="__main__":
    username = ""   #input("username:")
    pwd = ""    #input('password:')
    getDistrictName(username, pwd)
    # getTransList()
