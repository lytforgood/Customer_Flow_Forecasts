# -*- coding: utf-8 -*-
'''
星期特征
shopid  weekday  pay_count
取最近两周训练
'''
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
# from sklearn.gaussian_process import GaussianProcessRegressor #高斯回归做填充
import datetime

train_all = pd.read_csv("../../data/dataset/feature/train_all_weekday.csv",header=None)
train_all.columns=['shop_id','time','year','mouth','day','pay_count','pay_user_count','view_count','view_user_count','city_name','location_id','per_pay','score','comment_cnt','shop_level','cate_1_name','cate_2_name','cate_3_name','week_of_year','week_day']
train_all=train_all[['shop_id','time','week_day','pay_count']]
train_all=train_all[(train_all['time'].astype(int)<=20161031)&(train_all['time'].astype(int)>=20161011)].reset_index()
train_all=train_all[['shop_id','week_day','pay_count']]


test_all = pd.read_csv("../../data/dataset/feature/test_all_weekday.txt",header=None)
test_all.columns=['shop_id','time','location_id','per_pay','score','comment_cnt','shop_level','cate_1_name','cate_2_name','cate_3_name','week_day']
test_all=test_all[['shop_id','week_day']]

shop_id=train_all['shop_id'].drop_duplicates()
for s_id in shop_id:
  tmp=train_all[(train_all['shop_id']==s_id)].reset_index()
  test_tmp=test_all[(test_all['shop_id']==s_id)].reset_index()
  # clf=LinearRegression(fit_intercept=True, normalize=False, copy_X=True, n_jobs=1)
  clf =GradientBoostingRegressor(
    loss='ls'
  , learning_rate=0.1
  , n_estimators=500
  , subsample=1
  , min_samples_split=2
  , min_samples_leaf=1
  , max_depth=5
  , init=None
  , random_state=None
  , max_features=None
  , alpha=0.9
  , verbose=0
  , max_leaf_nodes=None
  , warm_start=False
  )
  clf.fit(tmp.iloc[:,2:3], tmp.iloc[:,3])
  test_pre = clf.predict(test_tmp.iloc[:,2:3])
  test_pre=pd.DataFrame({'test_pre':test_pre})
  test_re=pd.concat([test_tmp,test_pre],axis=1)
  test_re=test_re[['shop_id','week_day','test_pre']]
  # test_re.sort(['shop_id','week_day'],ascending=False)
  test_re.to_csv("../../data/dataset/feature/test_re.txt",header=False,mode='a',index=False)

print 'end'
