# -*- coding: utf-8 -*-
'''
数据 预处理(preprocessing)：
缺失值填充
类别标签处理
标签类别化 LabelEncoder
独热编码  OneHotEncoder
特征过程：
生成多项式特征PolynomialFeatures  原始特征：(x1,x2) 转化后(1,x1,x2,x1^2,x2^2,x1x2,x2^2)


'''
import pandas as pd
from sklearn import preprocessing
import datetime

# train_all = pd.read_csv("../../data//dataset/feature/train_all_null.txt",header=None)
train_all = pd.read_csv("../../data/dataset/feature/train_all.txt",header=None)
train_all.columns=['shop_id','time','year','mouth','day','pay_count','pay_user_count','view_count','view_user_count','city_name','location_id','per_pay','score','comment_cnt','shop_level','cate_1_name','cate_2_name','cate_3_name']


#标签类别化
tmp=train_all["city_name"]
le = preprocessing.LabelEncoder()
#将类别转变成编码类型
le.fit(tmp)
#list(le.classes_)
# for i in le.classes_:
#     print i
#将类别序列转变为编码
tmp=le.transform(tmp)
# list(le.inverse_transform([0, 2, 1]))
train_all['city_name']=tmp

tmp=train_all["cate_1_name"]
le.fit(tmp)
tmp=le.transform(tmp)
train_all['cate_1_name']=tmp

tmp=train_all["cate_2_name"]
le.fit(tmp)
tmp=le.transform(tmp)
train_all['cate_2_name']=tmp

tmp=train_all["cate_3_name"]
le.fit(tmp)
tmp=le.transform(tmp)
train_all['cate_3_name']=tmp

#OneHot 编码  eg:A样本在3个纬度下分别属于1,0,2的类别 转换成独热编码 [ 1.  1.  1.]
# onehot=[]
# for i in xrange(train_all.shape[0]) :
#   tmp=[]
#   tmp.append(train_all["cate_1_name"][i])
#   tmp.append(train_all["cate_2_name"][i])
#   tmp.append(train_all["cate_3_name"][i])
#   onehot.append(tmp)
# enc = preprocessing.OneHotEncoder()
# enc.fit(onehot)
# onehot_feature=enc.transform(onehot).toarray()
# onehot_feature=pd.DataFrame({'onehot':onehot})

#生成多项式特征
# X = np.arange(6).reshape(3, 2)
# poly = PolynomialFeatures(2) #poly = PolynomialFeatures(interaction_only=True)
# poly.fit_transform(X)

#标准化  from sklearn.preprocessing import StandardScaler z-score规范化:特征值减去均值，除以标准
# scaler = sklearn.preprocessing.StandardScaler().fit(train)
# scaler.transform(train)
# scaler.transform(test)

#最小-最大规范化 axis=0轴按列 np.sum(x,axis=0)  ((X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0)))* (max - min) + min  (x-x最小/x最大-x最小)*(规约的最大-规约的最小)+规约的最小
# from sklearn.preprocessing import MinMaxScaler
# min_max_scaler = MinMaxScaler()
# min_max_scaler.fit_transform(x)

#规范化（Normalization）规范化是将不同变化范围的值映射到相同的固定范围，常见的是[0,1]，此时也称为归一化
#默认L2规范 变换后每个样本的各维特征的平方和为1 0.4^2+0.4^2+0.81^2=1 L1 norm则是变换后每个样本的各维特征的绝对值和为1。还有max norm，则是将每个样本的各维特征除以该样本各维特征的最大值
# import sklearn
# X = [[ 1, -1, 2],[ 2, 0, 0], [ 0, 1, -1]]
# sklearn.preprocessing.normalize(X, norm='l2')
# array([[ 0.40, -0.40, 0.81], [ 1, 0, 0], [ 0, 0.70, -0.70]])

#特征二值化（Binarization） 大于阈值为1 小于阈值为0
# X = [1,2,0.5,0.1,4,5]
# binarizer = sklearn.preprocessing.Binarizer(threshold=1.1)
# binarizer.transform(X)

#标签二值化  将classes标注的标签所在位置标为1 其他位置标为0 几类就输出几维
# from sklearn.preprocessing import label_binarize
# label_binarize([1, 6], classes=[1, 2, 4, 6])  #输出[1, 0, 0, 0],[0, 0, 0, 1]
# label_binarize(['yes', 'no', 'no', 'yes'], classes=['no', 'yes'])


##判断为该年第几周 import datetime datetime.date(2017, 1, 16).isocalendar() 返回结果是三元组（年号，第几周，第几天） weekday 返回星期几 1-7
tmp=[]
weekday=[]
for i in xrange(train_all.shape[0]) :
    week_year=list(datetime.date(train_all['year'][i], train_all['mouth'][i], train_all['day'][i]).isocalendar())
    date_time = datetime.datetime.strptime(train_all['time'][i].astype('string'),'%Y%m%d')
    weekday.append(date_time.weekday()+1)
    tmp.append(str(week_year[0])+str(week_year[1]))
week_of_year=pd.DataFrame({'week_of_year':tmp})
week_day=pd.DataFrame({'week_day':weekday})
train_all=pd.concat([train_all,week_of_year],axis=1)
train_all=pd.concat([train_all,week_day],axis=1)

# train_all.to_csv("./train_all_weekday.csv",header=False,index=False)




