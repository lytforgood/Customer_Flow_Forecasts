# -*- coding: utf-8 -*-
import pandas as pd
#评测开始
real_all = pd.read_csv("../../data/dataset/feature/real_18_31.txt",header=None)
pre_all = pd.read_csv("../../data/dataset/feature/wnn_18_31.txt",header=None)

real_all.columns=['shop_id','day_1','day_2','day_3','day_4','day_5','day_6','day_7','day_8','day_9','day_10','day_11','day_12','day_13','day_14']
pre_all.columns=['shop_id','day_1','day_2','day_3','day_4','day_5','day_6','day_7','day_8','day_9','day_10','day_11','day_12','day_13','day_14']

real_all[['day_1','day_2','day_3','day_4','day_5','day_6','day_7','day_8','day_9','day_10','day_11','day_12','day_13','day_14']]=real_all[['day_1','day_2','day_3','day_4','day_5','day_6','day_7','day_8','day_9','day_10','day_11','day_12','day_13','day_14']].astype(float)
pre_all[['day_1','day_2','day_3','day_4','day_5','day_6','day_7','day_8','day_9','day_10','day_11','day_12','day_13','day_14']]=pre_all[['day_1','day_2','day_3','day_4','day_5','day_6','day_7','day_8','day_9','day_10','day_11','day_12','day_13','day_14']].astype(float)
# re = pd.merge(real_all,pre_all,on='shop_id',how='left')
# pre_all=pre_all.fillna(0)
shop_id=real_all['shop_id']
def shop_id_sum(rel_list,pre_list) :
  tmp_sum=0.0
  for i in xrange(len(rel_list)):
      if (rel_list[i] !=0.0) & (pre_list[i] !=0.0):
         tmp_sum=tmp_sum+abs((pre_list[i]-rel_list[i])/(pre_list[i]+rel_list[i]))
      else :
         tmp_sum=tmp_sum+0.0
  return tmp_sum
error=0.0
shop_id_error=[]
for s_id in shop_id:
    x=list(real_all[(real_all['shop_id']==s_id)].iloc[0,1:15])
    y=list(pre_all[(pre_all['shop_id']==s_id)].iloc[0,1:15])
    shop_id_error.append(shop_id_sum(x,y))
    error=error+shop_id_sum(x,y)
re=error/(len(shop_id)*14)
print(re)
# err=pd.DataFrame({'error':shop_id_error})
# re_tail=pd.concat([shop_id,err],axis=1)
# 按误差大小排序
# re_tail.sort(['error'],ascending=False)
