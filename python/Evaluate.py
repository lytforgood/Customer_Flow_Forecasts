# -*- coding: utf-8 -*-
'''
1.构建预测集合
2.评价函数
'''
import pandas as pd
#构建预测集合
train_all = pd.read_csv("../../data/dataset/feature/train_all.txt",header=None)
train_all.columns=['shop_id','time','year','mouth','day','pay_count','pay_user_count','view_count','view_user_count','city_name','location_id','per_pay','score','comment_cnt','shop_level','cate_1_name','cate_2_name','cate_3_name']

tmp=train_all[(train_all['time']<=20161031)&(train_all['time']>=20161018)].reset_index()
shop_id = train_all['shop_id']
shop_id = shop_id.drop_duplicates()
re=[]
for s_id in shop_id :
    t=tmp[(tmp['shop_id']==s_id)].sort(["time"]).reset_index()
    tmp2=''
    for i in list(t['pay_count']):
      tmp2=tmp2+','+str(i)
    out=str(s_id)+tmp2
    re.append(out)

#list每个元素按行写入文本
def list_to_file_bylines(path,list_data) :
  file=open(path,'w')
  for i in list_data:
      file.write(i)
      file.write("\n")
  file.close()
  print('ok')

list_to_file_bylines('../../data/dataset/feature/re_test.txt',re)


#评测开始
real_all = pd.read_csv("../../data/dataset/feature/re_test.txt",header=None)
real_all.columns=['shop_id','day_1','day_2','day_3','day_4','day_5','day_6','day_7','day_8','day_9','day_10','day_11','day_12','day_13','day_14']
pre_all = pd.read_csv("../../data/dataset/feature/re_test.txt",header=None)
pre_all.columns=['shop_id','day_1','day_2','day_3','day_4','day_5','day_6','day_7','day_8','day_9','day_10','day_11','day_12','day_13','day_14']

real_all[['day_1','day_2','day_3','day_4','day_5','day_6','day_7','day_8','day_9','day_10','day_11','day_12','day_13','day_14']]=real_all[['day_1','day_2','day_3','day_4','day_5','day_6','day_7','day_8','day_9','day_10','day_11','day_12','day_13','day_14']].astype(float)
pre_all[['day_1','day_2','day_3','day_4','day_5','day_6','day_7','day_8','day_9','day_10','day_11','day_12','day_13','day_14']]=pre_all[['day_1','day_2','day_3','day_4','day_5','day_6','day_7','day_8','day_9','day_10','day_11','day_12','day_13','day_14']].astype(float)
#缺失值填充
real_all=real_all.fillna(0)
pre_all=pre_all.fillna(0)
# re = pd.merge(real_all,pre_all,on='shop_id',how='left')
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
err=pd.DataFrame({'error':shop_id_error})
re_tail=pd.concat([shop_id,err],axis=1)
# err[pd.isnull(err['error'])].head()
# real_all.iloc([151,1:15])
real_all=real_all.sort(['shop_id'],ascending=True)
real_all.to_csv("../../data/dataset/feature/test_18_31.txt",header=False,index=False)
