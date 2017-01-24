# -*- coding: utf-8 -*-
'''
数据合并
补充缺失日期
缺失值填充一部分
处理天气
'''

import pandas as pd
import datetime

##读取scala解析后的结果
shop_info = pd.read_csv("../../data/dataset/shop_info.txt",header=None)
shop_info.columns=['shop_id','city_name','location_id','per_pay','score','comment_cnt','shop_level','cate_1_name','cate_2_name','cate_3_name']
user_pay = pd.read_csv("../../data//dataset/feature/商家每天支付的支付次数.txt",header=None)
user_pay.columns=['shop_id','time','year','mouth','day','pay_count']
user_pay2 = pd.read_csv("../../data//dataset/feature/商家每天支付的用户个数.txt",header=None)
user_pay2.columns=['shop_id','time','year','mouth','day','pay_user_count']
user_view = pd.read_csv("../../data//dataset/feature/商家每天浏览的浏览次数.txt",header=None)
user_view.columns=['shop_id','time','year','mouth','day','view_count']
user_view2 = pd.read_csv("../../data//dataset/feature/商家每天浏览的用户人数.txt",header=None)
user_view2.columns=['shop_id','time','year','mouth','day','view_user_count']
#合并数据源
user_pay_all = pd.merge(user_pay,user_pay2,on=['shop_id','time','year','mouth','day'],how='left')
user_view_all= pd.merge(user_view,user_view2,on=['shop_id','time','year','mouth','day'],how='left')
#删除无用变量
del user_pay
del user_pay2
del user_view
del user_view2
#输出中间结果
# user_pay_all.to_csv("../../data//dataset/feature/user_pay_all.csv",header=False,index=False)
# user_view_all.to_csv("../../data//dataset/feature/user_view_all.csv",header=False,index=False)
shop_id = user_pay_all['shop_id']
shop_id = shop_id.drop_duplicates()

#获取时间序列(返回整型list)
def datelist(start, end):
    start_date = datetime.date(*start)
    end_date = datetime.date(*end)

    result = []
    curr_date = start_date
    while curr_date != end_date:
        ymd="%04d%02d%02d" % (curr_date.year, curr_date.month, curr_date.day)
        result.append(int(ymd))
        curr_date += datetime.timedelta(1)
    result.append(int(ymd))
    return result

alltime_set=set(datelist((2016, 7, 1), (2016, 10, 31)))

add_01=[]
add_02=[]
add_03=[]
add_04=[]
add_05=[]
add_06=[]
add_07=[]
for s_id in shop_id :
    tmp=user_pay_all[(user_pay_all['shop_id']==s_id)]
    time_set=set(tmp['time'])
    cha=alltime_set-time_set
    for c in cha :
      add_01.append(s_id)
      add_02.append(c)
      add_03.append(int(str(c)[0:4]))
      add_04.append(int(str(c)[4:6]))
      add_05.append(int(str(c)[6:8]))
      add_06.append(0)
      add_07.append(0)
#补充的结果
add_all=pd.DataFrame({'shop_id':add_01,'time':add_02,'year':add_03,'mouth':add_04,'day':add_05,'pay_count':add_06,'pay_user_count':add_07})
columns = ['shop_id','time','year','mouth','day','pay_count','pay_user_count']
add_all=add_all.ix[:,columns]
user_pay_all=pd.concat([user_pay_all,add_all])
##继续合并
train_view = pd.merge(user_view_all,shop_info,on=['shop_id'],how='left')
train_pay = pd.merge(user_pay_all,shop_info,on=['shop_id'],how='left')

train_all =pd.merge(user_pay_all,user_view_all,on=['shop_id','time','year','mouth','day'],how='left')
train_all_2=pd.merge(train_all,shop_info,on=['shop_id'],how='left')

# 输出含缺失值的汇总文件
# train_all_2.to_csv("../../data//dataset/feature/train_all_null.txt",header=False,index=False)


#缺失值处理  view_count
#查看缺失值
train_all_2[pd.isnull(train_all_2["view_count"])].head()
#view_count 填充为0
train_all_2["view_count"]=train_all_2["view_count"].fillna(0)  #填充缺失值
#view_user_count
train_all_2["view_user_count"]=train_all_2["view_user_count"].fillna(0)  #填充缺失值
#score  评分 填充为均值？ 某类均值？ round(a,1) 保留小数点后1位
tmp=round(train_all_2[-pd.isnull(train_all_2["score"])]["score"].mean(),1)
train_all_2["score"]=train_all_2["score"].fillna(tmp)
#comment_cnt 评论数 填充为均值？ 某门店等级一级品类名称二级分类名称的均值？
tmp=round(train_all_2[-pd.isnull(train_all_2["comment_cnt"])]["comment_cnt"].mean(),1)
train_all_2["comment_cnt"]=train_all_2["comment_cnt"].fillna(tmp)
#cate_3_name 三级分类名称 标记为缺失
tmp="缺失"
train_all_2["cate_3_name"]=train_all_2["cate_3_name"].fillna(tmp)

#保存结果
train_all_2.to_csv("../../data/dataset/feature/train_all.txt",header=False,index=False)

#处理天气
weather = pd.read_csv("../../data/dataset/feature/ijcai17-wheather.csv",header=None)
weather.columns=['city_name','date','topTemp','lowTemp','weather','wind','windStrength','no']
date_time=weather['date']
time=[]
for dt in date_time:
  time.append(int(dt[0:4]+dt[5:7]+dt[8:10]))
time=pd.DataFrame({'time':time})
weather=pd.concat([weather[['city_name','date','topTemp','lowTemp','weather','wind','windStrength']],time],axis=1)

train_all_2=pd.merge(train_all_2,weather,on=['city_name','time'],how='left')
train_all_2=train_all_2[['shop_id','time','year','mouth','day','pay_count','pay_user_count','view_count','view_user_count','city_name','location_id','per_pay','score','comment_cnt','shop_level','cate_1_name','cate_2_name','cate_3_name','topTemp','lowTemp','weather','wind','windStrength']]

train_all_2.to_csv("../../data/dataset/feature/train_all_weather.txt",header=False,index=False)
