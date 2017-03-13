# -*- coding: utf-8 -*-
'''
构建测试集合常规特征
'''
import pandas as pd
from sklearn import preprocessing
import datetime

train_all = pd.read_csv("../../data/dataset/feature/train_all.txt",header=None)
train_all.columns=['shop_id','time','year','mouth','day','pay_count','pay_user_count','view_count','view_user_count','city_name','location_id','per_pay','score','comment_cnt','shop_level','cate_1_name','cate_2_name','cate_3_name']

test_shop=train_all[['shop_id','location_id','per_pay','score','comment_cnt','shop_level','cate_1_name','cate_2_name','cate_3_name']].drop_duplicates().reset_index()

#生成时间序列
def datelist(start, end):
    start_date = datetime.date(*start)
    end_date = datetime.date(*end)

    result = []
    curr_date = start_date
    while curr_date != end_date:
        result.append("%04d%02d%02d" % (curr_date.year, curr_date.month, curr_date.day))
        curr_date += datetime.timedelta(1)
    result.append("%04d%02d%02d" % (curr_date.year, curr_date.month, curr_date.day))
    return result
test_time=datelist((2016,11,1), (2016,11,7))
for i in test_time :
  time1=[]
  for j in range(test_shop.shape[0]):
    time1.append(i)
  time1=pd.DataFrame({'time1':time1})
  test1=pd.concat([test_shop,time1],axis=1)
  test1.to_csv("../../data/dataset/feature/test_all.txt",header=False,mode='a',index=False) #a追加


test_all = pd.read_csv("../../data/dataset/feature/test_all.txt",header=None)
test_all.columns=['index','shop_id','location_id','per_pay','score','comment_cnt','shop_level','cate_1_name','cate_2_name','cate_3_name','time']
weekday=[]
for i in xrange(test_all.shape[0]) :
    date_time = datetime.datetime.strptime(test_all['time'][i].astype('string'),'%Y%m%d')
    weekday.append(date_time.weekday()+1)
week_day=pd.DataFrame({'week_day':weekday})
test_all=pd.concat([test_all,week_day],axis=1)

test_all=test_all[['shop_id','time','location_id','per_pay','score','comment_cnt','shop_level','cate_1_name','cate_2_name','cate_3_name','week_day']]
test_all.to_csv("../../data/dataset/feature/test_all_weekday.txt",header=False,index=False)
