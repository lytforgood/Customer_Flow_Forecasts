# -*- coding: utf-8 -*-
'''
提取特征+模型训练
#shop_id 特征
1、位置接近的商家有几家
2、所在城市同一级品类名称的有几家
3、所在城市相同一级品类名称and二级分类名称的有几家

4、人均消费
5、评分
6、评论数
7、门店等级

#支付特征
最近一个月/一周的总支付次数
最近一个月/一周的每天的支付次数
最近一个月/一周的总支付人数
最近一个月/一周的每天的支付人数
所在城市同一级品类名称的最近一个月/一周的每天的支付次数
#浏览特征
最近一个月/一周的总浏览次数
最近一个月/一周的每天的浏览次数
最近一个月/一周的总浏览人数
最近一个月/一周的每天的浏览人数
所在城市同一级品类名称的最近一个月/一周的每天的浏览次数
#日期特征
是否工作日
周几
去年一周的均值/去年今天的值
'''

import pandas as pd
from sklearn import preprocessing
# from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingRegressor
# from sklearn.linear_model import Ridge
# from sklearn.linear_model import Lasso
# from sklearn.linear_model import ElasticNet
# from sklearn.tree import DecisionTreeRegressor
# from sklearn.ensemble import ExtraTreesRegressor
# from sklearn.ensemble import AdaBoostRegressor
# from sklearn.ensemble import GradientBoostingRegressor
# from xgboost import XGBRegressor
# from xgboost import XGBClassifier
import datetime

train_all = pd.read_csv("../../data/dataset/feature/train_all_weekday.csv",header=None)
train_all.columns=['shop_id','time','year','mouth','day','pay_count','pay_user_count','view_count','view_user_count','city_name','location_id','per_pay','score','comment_cnt','shop_level','cate_1_name','cate_2_name','cate_3_name','week_of_year','week_day']

test_all = pd.read_csv("../../data/dataset/feature/test_all_weekday.txt",header=None)
test_all.columns=['shop_id','time','location_id','per_pay','score','comment_cnt','shop_level','cate_1_name','cate_2_name','cate_3_name','week_day']

#按照商铺类型分别建模
shop_class=train_all[['cate_1_name','cate_2_name','cate_3_name']]
shop_class=shop_class.drop_duplicates()
shop_class.index=[i for i in range(shop_class.shape[0])]
#训练集合-20161018-31
for i in range(shop_class.shape[0]):
  print i
  train_shop=train_all[(train_all['cate_1_name']==shop_class['cate_1_name'][i])&(train_all['cate_2_name']==shop_class['cate_2_name'][i])&(train_all['cate_3_name']==shop_class['cate_3_name'][i])].reset_index()
  train_shop=train_shop[(train_shop['time'].astype(int)<=20161031)&(train_shop['time'].astype(int)>=20161018)].reset_index()
  #shop_id 特征
  feature_shop=train_shop[['shop_id','time','location_id','per_pay','score','comment_cnt','shop_level','pay_count','pay_user_count','view_count','view_user_count','week_day']].drop_duplicates().sort(["shop_id"]).reset_index()
  #支付特征
  feature1=[]
  feature2=[]
  feature3=[]
  feature4=[]
  feature5=[]
  feature6=[]
  feature7=[]
  feature8=[]
  #最近两周/一周的总支付次数/均值
  for j in range(feature_shop.shape[0]):
    init_data=feature_shop['time'][j]
    tmp_data = datetime.datetime.strptime(str(init_data),'%Y%m%d')
    last_time = tmp_data - datetime.timedelta(days=14)
    last_time = int(datetime.datetime.strftime(last_time,'%Y%m%d'))
    tmp=train_all[(train_all['time'].astype(int)<init_data)&(train_all['time'].astype(int)>=last_time)&(train_all['week_day']==feature_shop['week_day'][j])&(train_all['shop_id']==feature_shop['shop_id'][j])]
    feature1.append(tmp['pay_count'].sum())
    feature2.append(int(tmp['pay_count'].mean()))
    #最近两周/一周的总支付人数/均值
    feature3.append(tmp['pay_user_count'].sum())
    feature4.append(int(tmp['pay_user_count'].mean()))
    #最近两周/一周的总浏览次数/均值
    feature5.append(tmp['view_count'].sum())
    feature6.append(int(tmp['view_count'].mean()))
    #最近两周/一周的总浏览人数/均值
    feature7.append(tmp['view_user_count'].sum())
    feature8.append(int(tmp['view_user_count'].mean()))
    # feature1=tmp.groupby(['shop_id'])['pay_count'].sum().reset_index()
    # feature2=tmp.groupby(['shop_id'])['pay_count'].mean().astype(int).reset_index()
    # feature2.sort(["shop_id"])
    #最近两周/一周的总支付人数/均值
    # feature3=tmp.groupby(['shop_id'])['pay_user_count'].sum().reset_index()
    # feature4=tmp.groupby(['shop_id'])['pay_user_count'].mean().astype(int).reset_index()
    # #最近两周/一周的总浏览次数/均值
    # feature5=tmp.groupby(['shop_id'])['view_count'].sum().reset_index()
    # feature6=tmp.groupby(['shop_id'])['view_count'].mean().astype(int).reset_index()
    # #最近两周/一周的总浏览人数/均值
    # feature7=tmp.groupby(['shop_id'])['view_user_count'].sum().reset_index()
    # feature8=tmp.groupby(['shop_id'])['view_user_count'].mean().astype(int).reset_index()

  feature1=pd.DataFrame({'pay_count_sum':feature1})
  feature2=pd.DataFrame({'pay_count_mean':feature2})
  feature3=pd.DataFrame({'pay_user_count_sum':feature3})
  feature4=pd.DataFrame({'pay_user_count_mean':feature4})
  feature5=pd.DataFrame({'view_count_sum':feature5})
  feature6=pd.DataFrame({'view_count_mean':feature6})
  feature7=pd.DataFrame({'view_user_count_sum':feature7})
  feature8=pd.DataFrame({'view_user_count_mean':feature8})
  train_shop_all=pd.concat([train_shop,feature1,feature2,feature3,feature4,feature5,feature6,feature7,feature8],axis=1)#.sort(["shop_id"])
  train_shop_all=train_shop_all[['shop_id','per_pay','score','comment_cnt','shop_level','week_day','pay_count_sum','pay_count_mean','pay_user_count_sum','pay_user_count_mean','view_count_sum','view_count_mean','view_user_count_sum','view_user_count_mean','pay_count']]

  ##构建测试集合
  feature_shop=test_all[(test_all['cate_1_name']==shop_class['cate_1_name'][i])&(test_all['cate_2_name']==shop_class['cate_2_name'][i])&(test_all['cate_3_name']==shop_class['cate_3_name'][i])].reset_index()
  feature1=[]
  feature2=[]
  feature3=[]
  feature4=[]
  feature5=[]
  feature6=[]
  feature7=[]
  feature8=[]
  for j in range(feature_shop.shape[0]):
    init_data=feature_shop['time'][j]
    tmp_data = datetime.datetime.strptime(str(init_data),'%Y%m%d')
    last_time = tmp_data - datetime.timedelta(days=14)
    last_time = int(datetime.datetime.strftime(last_time,'%Y%m%d'))
    tmp=train_all[(train_all['time'].astype(int)<init_data)&(train_all['time'].astype(int)>=last_time)&(train_all['week_day']==feature_shop['week_day'][j])&(train_all['shop_id']==feature_shop['shop_id'][j])]
    feature1.append(tmp['pay_count'].sum())
    feature2.append(int(tmp['pay_count'].mean()))
    #最近两周/一周的总支付人数/均值
    feature3.append(tmp['pay_user_count'].sum())
    feature4.append(int(tmp['pay_user_count'].mean()))
    #最近两周/一周的总浏览次数/均值
    feature5.append(tmp['view_count'].sum())
    feature6.append(int(tmp['view_count'].mean()))
    #最近两周/一周的总浏览人数/均值
    feature7.append(tmp['view_user_count'].sum())
    feature8.append(int(tmp['view_user_count'].mean()))
  feature1=pd.DataFrame({'pay_count_sum':feature1})
  feature2=pd.DataFrame({'pay_count_mean':feature2})
  feature3=pd.DataFrame({'pay_user_count_sum':feature3})
  feature4=pd.DataFrame({'pay_user_count_mean':feature4})
  feature5=pd.DataFrame({'view_count_sum':feature5})
  feature6=pd.DataFrame({'view_count_mean':feature6})
  feature7=pd.DataFrame({'view_user_count_sum':feature7})
  feature8=pd.DataFrame({'view_user_count_mean':feature8})
  test_shop_all=pd.concat([feature_shop,feature1,feature2,feature3,feature4,feature5,feature6,feature7,feature8],axis=1)#.sort(["shop_id"])
  test_shop_all=test_shop_all[['shop_id','per_pay','score','comment_cnt','shop_level','week_day','pay_count_sum','pay_count_mean','pay_user_count_sum','pay_user_count_mean','view_count_sum','view_count_mean','view_user_count_sum','view_user_count_mean','week_day']]

  ##模型训练 LR  GBDT
  # # clf = Ridge(alpha=1.0,random_state=seed) #0.841269 0.732074
# # clf = Lasso(alpha=0.001,random_state=seed) #0.834484 0.716615
# # clf = ElasticNet(alpha=0.001,random_state=seed) #0.829437 0.716322
# # clf = DecisionTreeRegressor(max_depth=5,random_state=seed) #0.635430 0.531403
# # clf = ExtraTreesRegressor(n_jobs=-1,n_estimators=100,random_state=seed) #0.649415 0.544799
# # clf = AdaBoostRegressor(n_estimators=100,random_state=seed) #0.635245 0.531407
# # clf = GradientBoostingRegressor(n_estimators=50,random_state=seed) #0.562742 0.474085
# # clf = XGBRegressor(n_estimators=1000,seed=seed) #0.718094 0.558765
# # clf = XGBClassifier(n_estimators=1000,seed=seed)  #0.672249 0.588265
  # clf = LogisticRegression(penalty='l2', C=2)
  clf = GradientBoostingRegressor(n_estimators=200,random_state=1)
  clf.fit(train_shop_all.iloc[:,5:14], train_shop_all.iloc[:,14])
  test_pre = clf.predict(test_shop_all.iloc[:,5:14])
  test_pre=pd.DataFrame({'test_pre':test_pre})
  test_re=pd.concat([test_shop_all,test_pre],axis=1)
  test_re=test_re[['shop_id','week_day','test_pre']]
  # test_re.sort(['shop_id','week_day'],ascending=False)
  test_re.to_csv("../../data/dataset/feature/test_re.txt",header=False,mode='a',index=False)

print '结束'
