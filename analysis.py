import pandas as pd
import numpy as np
import pylab
import os

# cities = ['bj', 'cd', 'cq', 'cs', 'dl', 'dg', 'fs','gz','hz','hui','hk','jn','jx','lin','nj', 'nt','qd','sz','sjz','sy','tj','ts','ty','wh','wx','wf','wz','xa','xm','xz','yt','yz','zs','zh']

def GroupColFunc(df, ind, col):
	if(df[col].loc[ind][0:7]>='2015.00'):
		return df[col].loc[ind][0:7]
	else:
		return '-'

t = pd.read_csv('./quanguo1/chengjiao_list/bj.csv', encoding='gbk')
# hall_room_unitPrice = t.groupby(['hallNum','roomNum'])['unitPrice'].mean()
# print(type(hall_room_unitPrice))
# hall_room_unitPrice.plot()
# pylab.show()
signTime_unitPrice = t.groupby(lambda x: GroupColFunc(t, x, 'signTime'))['unitPrice'].mean()
# print(signTime_unitPrice)
signTime_unitPrice.plot()
pylab.show()
resblock_name = t['resblockName'].unique()
	# resblockName = t['resblockName']
	# signTime = t['signTime']
	# unitPrice = t['unitPrice']
	# signPrice = t['signPrice']
	# houseArea = t['houseArea']
	# soleString = t['soleString']
	# frameOrientation = t['frameOrientation']
	# floorInfo = t['floorInfo']
	# subTitle = t['subTitle']
	# subwayInfoString = t['subwayInfoString']
	# finishYear = t['finishYear']
	# decorationType = t['decorationType']
	# hallNum = t['hallNum']
	# roomNum = t['roomNum']
# 	if(len(resblock_name) == 0):
# 		print(filename, '\' xiaoqu_name length is 0')
# 	elif resblock_name[0] not in xiaoqu_name:
# 		xiaoqu_name[resblock_name[0]] = 1
# 		schoolInfoString.extend(t['schoolInfoString'])
# 		houseArea.extend(t['houseArea'])
# 		year.extend(t['year'])
# 		buildingType.extend(t['buildingType'])
# 		houseUrl.extend(t['houseUrl'])
# 		otherSourceUnitPriceMin.extend(t['otherSourcePriceMin'])
# 		soleString.extend(t['soleString'])
# 		unitPrice.extend(t['unitPrice'])
# 		fluctuation.extend(t['fluctuation'])
# 		resblockName.extend(t['resblockName']) 
# 		resblockID.extend(t['resblockID']) 
# 		otherSourcePriceMin.extend(t['otherSourcePriceMin'])
# 		otherSourceUnitPriceMax.extend(t['otherSourceUnitPriceMax'])
# 		frameOrientation.extend(t['frameOrientation'])
# 		isDisplay.extend(t['isDisplay'])
# 		floorInfo.extend(t['floorInfo'])
# 		listPicUrl.extend(t['listPicUrl'])
# 		subTitle.extend(t['subTitle'])
# 		signTime.extend(t['signTime'])
# 		subwayInfoString.extend(t['subwayInfoString'])
# 		finishYear.extend(t['finishYear'])
# 		houseCode.extend(t['houseCode']) 
# 		signSourceText.extend(t['signSourceText'])
# 		signPrice.extend(t['signPrice'])
# 		sameFrameUrl.extend(t['sameFrameUrl'])
# 		signSource.extend(t['signSource'])
# 		hallNum.extend(t['hallNum'])
# 		titleString.extend(t['titleString'])
# 		decorationType.extend(t['decorationType'])
# 		signSourceId.extend(t['signSourceId']) 
# 		roomNum.extend(t['roomNum'])
# 		framePicUrl.extend(t['framePicUrl'])
# 		# print(len(t['picNum']))
# 		# print(type(list(t['picNum'])))
# 		picNum.extend(t['picNum'])
# 	else:
# 		k+=1

# print(k)
# print(len(roomNum))
# raw_data =  {'schoolInfoString':schoolInfoString, 'houseArea':houseArea, 'year':year, 'buildingType':buildingType,\
# 			 			'houseUrl':houseUrl, 'otherSourceUnitPriceMin':otherSourceUnitPriceMin, 'soleString':soleString, 'unitPrice':unitPrice, \
# 			 			'fluctuation':fluctuation, 'resblockName':resblockName, 'resblockID':resblockID, 'otherSourcePriceMin':otherSourcePriceMin,\
# 			  			'otherSourceUnitPriceMax':otherSourceUnitPriceMax, 'frameOrientation':frameOrientation, 'isDisplay':isDisplay,\
# 			   			'floorInfo':floorInfo, 'listPicUrl':listPicUrl, 'subTitle':subTitle, 'signTime':signTime,\
# 			   			'subwayInfoString':subwayInfoString, 'finishYear':finishYear, 'houseCode':houseCode, 'signSourceText':signSourceText,\
# 			   			'signPrice':signPrice, 'sameFrameUrl':sameFrameUrl, 'signSource':signSource, 'hallNum':hallNum,\
# 			   			'titleString':titleString, 'decorationType':decorationType, 'signSourceId':signSourceId, 'roomNum':roomNum, \
# 			   			'framePicUrl':framePicUrl,'picNum':picNum}
# df = pd.DataFrame(raw_data, columns=['schoolInfoString', 'houseArea', 'year', 'buildingType', 'houseUrl', 'otherSourceUnitPriceMin', 'soleString', \
# 			'unitPrice', 'fluctuation', 'resblockName', 'resblockID', 'otherSourcePriceMin', 'otherSourceUnitPriceMax', \
# 			'frameOrientation', 'isDisplay', 'floorInfo', 'listPicUrl', 'subTitle', 'signTime', 'subwayInfoString', \
# 			'finishYear', 'houseCode', 'signSourceText', 'signPrice', 'sameFrameUrl', 'signSource', 'hallNum', 'titleString', \
# 			'decorationType', 'signSourceId', 'roomNum', 'framePicUrl','picNum'])
# df.to_csv('./quanguo1/chengjiao_list/bj.csv')
# avgCost = []
# for k in range(len(cities)):
# 	# print(cities[k])
# 	try:
# 		df = pd.read_csv('./quanguo1/'+cities[k]+'.csv', header=0, encoding='gbk')
# 		# print(df.describe())
# 		avgCost.append(np.asarray(df[(df['measuring']=='万/套')]['avgCost'], dtype=np.float).mean())
# 	except IndexError:
# 		print('city name is', cities[k])

# raw_data={'city':cities, 'avgCost':avgCost}
# df = pd.DataFrame(raw_data, columns=['city','avgCost'])
# df.plot(x='city', y='avgCost', kind='bar', title='quanguo average xiaoqu cost')
# pylab.show()
# df.to_csv('lianjia.csv')