#时序模型
options(stringsAsFactors=F,scipen=99)
rm(list=ls());gc()
library(sqldf)
require(data.table)
library(recharts)
# da<- fread("/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/feature/train_all.txt",header = FALSE)
da<- fread("/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/feature/train_all_weekday.csv",header = FALSE)
#测试集选择的 20161018-20161031
#预测区间    2016.11.01-2016.11.14


#1.选两周的情况 --20161004-20161017  含国庆 应该不准  应该含有空缺值 补0(python已做)
re=sqldf("select V1,V2,V6 from da where V2>=20161004 and V2<=20161017 order by V1,V2")
shop_id=unique(da$V1)
out={}
for (i in 1:length(shop_id)){
tmp=re[which(re$V1==shop_id[i]),]
if(length(tmp$V6)!=14){
  print(shop_id[i])
  # print(length(tmp$V6))
}
a=c(shop_id[i],tmp$V6)
out=rbind(out,a)
}
write.table (out, file ="/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/feature/two_18_31.txt",sep =",",row.names = F,col.names=F,quote =F)
#选一周x2  2016.10.18-2016.10.24  2016.9.06-2016.9.12
re=sqldf("select V1,V2,V6 from da where V2>=20161018 and V2<=20161024 order by V1,V2")
shop_id=unique(da$V1)
out={}
for (i in 1:length(shop_id)){
tmp=re[which(re$V1==shop_id[i]),]
a=c(shop_id[i],tmp$V6,tmp$V6)
out=rbind(out,a)
}
out=as.data.frame(out)
out=sqldf("select * from out order by V1")
write.table (out, file ="/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/out/10_18_24x2.csv",sep =",",row.names = F,col.names=F,quote =F)

#2.前两周的均值
avg_re=sqldf("select V1,avg(V6) as r1 from da where V2>=20161018 and V2<=20161031 group by V1")
shop_id=unique(avg_re$V1)
out={}
for (i in 1:length(shop_id)){
tmp=avg_re[which(avg_re$V1==shop_id[i]),]
a=c(as.character(shop_id[i]),rep(floor(tmp$r1),14))
out=rbind(out,a)
}
out=as.data.frame(out)
# out=sqldf("select * from out order by V1")
out$V1=as.integer(out$V1)
out=sqldf("select * from out order by V1")
write.table (out, file ="/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/feature/twoavg_18_31.txt",sep =",",row.names = F,col.names=F,quote =F)
#前三周均值 小于20用进一法 大于20四舍五入
re=sqldf("select * from da where V2>=20161011")
shop_id=unique(re$V1)
out={}
for (i in 1:length(shop_id)){
tmp=re[which(re$V1==shop_id[i]),]
a=mean(tmp$V6)
if(a>=20){
a=round(a,0)
  }else{
a=ceiling(a)
  }
a=c(as.character(shop_id[i]),rep(a,14))
out=rbind(out,a)
}
out=as.data.frame(out)
out$V1=as.integer(out$V1)
out=sqldf("select * from out order by V1")
write.table (out, file ="/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/out/avg21_01.csv",sep =",",row.names = F,col.names=F,quote =F)

#每星期几的均值--去掉0[因为处理的时候补0了]--可以考虑去掉异常假日 / 去异常均值
da<- fread("/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/feature/train_all_weekday.csv",header = FALSE)
da=sqldf("select * from da where V2>=20160901")
da=sqldf("select * from da where V2>=20161011")
weekday=c(c(2:7),c(1))
shop_id=unique(da$V1)
out={}
for (i in 1:length(shop_id)){
avgre=da[which(da$V1==shop_id[i]),]
pre={}
for (j in 1:length(weekday)){
tmp=avgre[which(avgre$V20==weekday[j]),]
# a=tmp$V6
# a=floor(boxplot.stats(a)$conf[1])
# a=floor(mean(a))
a=mean(tmp$V6)
if(a>=20){
a=round(a,0)
  }else{
a=ceiling(a)
  }
# a=floor(median(a))
if(a>0){
  a=a
}else{
  a=0
}
pre=cbind(pre,a)
}
pre=c(as.character(shop_id[i]),pre,pre)
out=rbind(out,pre)
}
out=as.data.frame(out)
# out=sqldf("select * from out order by V1")
out$V1=as.integer(out$V1)
out=sqldf("select * from out order by V1")

write.table (out, file ="/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/out/avg21_weekday.csv",sep =",",row.names = F,col.names=F,quote =F)
write.table (out, file ="/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/out/avg60_weekdayx2_4.csv",sep =",",row.names = F,col.names=F,quote =F)
da<- fread("/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/out/avg_weekdayx2_2.csv",header = FALSE)
re=sqldf("select * from da order by V1")

write.table (re, file ="/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/out/avg_weekdayx2.csv",sep =",",row.names = F,col.names=F,quote =F)
#3.三阶指数平滑  选取前1个月的进行训练
re=sqldf("select V1,V2,V6 from da where V2>=20160919 and V2<=20161017 order by V1,V2")
re=sqldf("select V1,V2,V6 from da where V2>=20161001 and V2<=20161031 order by V1,V2")
shop_id=unique(da$V1)
out={}
for (i in 1:length(shop_id)){
tmp=re[which(re$V1==shop_id[i]),]
a=tmp$V6
#alpha不指定,beta=不指定,gamma不指定 三阶指数平滑 seasonal="additive"默认加法模型 "multiplicative"乘法模型
rp=HoltWinters(a,beta=F,gamma=F)
# pre=rp$coefficients
# pre <- predict(rp, 14, prediction.interval = TRUE)
# plot(rp, pre)
pre <- predict(rp, 14)
a=c(as.character(shop_id[i]),pre)
out=rbind(out,a)
}
write.table (out, file ="/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/feature/holt_18_31.txt",sep =",",row.names = F,col.names=F,quote =F)
write.table (out, file ="/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/out/holt_01_14.txt",sep =",",row.names = F,col.names=F,quote =F)

#取整
da<- fread("/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/out/holt_01_14.csv",header = FALSE)
re=sqldf("select V1,floor(V2),floor(V3),floor(V4),floor(V5),floor(V6),floor(V7),floor(V8),floor(V9),floor(V10),floor(V11),floor(V12),floor(V13),floor(V14),floor(V15) from da order by V1")
write.table (re, file ="/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/out/holt_01_14.csv",sep =",",row.names = F,col.names=F,quote =F)

# prophet 新方法Facebook
##参考http://blog.csdn.net/sinat_26917383/article/details/57419862
# library(prophet)
# https://github.com/facebookincubator/prophet
options(stringsAsFactors=F,scipen=99)
rm(list=ls());gc()
library(sqldf)
require(data.table)
library(recharts)
da<- fread("/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/feature/train_all_weekday.csv",header = FALSE)
library(prophet)
re=sqldf("select V1,V2,V6 from da where V2>=20161001 and V2<=20161017 order by V1,V2")
# rm(da)
shop_id=c(1:2000)
#
for (i in 1:length(shop_id)){
out={}
tmp=re[which(re$V1==shop_id[i]),]
history <- data.frame(ds = seq(as.Date('2016-10-01'), as.Date('2016-10-17'), by = 'd'),y=tmp$V6)
m <- prophet(history,growth = "linear") #线性趋势+趋势分解
future <- make_future_dataframe(m, periods = 7) #预测7天
# tail(future)
forecast <- predict(m, future)
# tail(forecast[c('ds', 'yhat', 'yhat_lower', 'yhat_upper')])
# #直线预测
# plot(m, forecast)
# #趋势分解
# prophet_plot_components(m, forecast)
pre=ceiling(forecast$yhat[(length(forecast$yhat)-7):length(forecast$yhat)])
a=c(as.character(shop_id[i]),pre,pre)
out=rbind(out,a)
out=as.data.frame(out)
write.table (out, file ="/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/out/testx1.csv",sep =",",row.names = F,col.names=F,quote =F,append=TRUE)
}
# out=as.data.frame(out)
# # out=sqldf("select * from out order by V1")
# out$V1=as.integer(out$V1)
# out=sqldf("select * from out order by V1")



#4.stl分解-以鲁棒局部加权回归作为平滑方法的时间序列分解方法
library(forecast)
re=sqldf("select V1,V2,V6 from da where V2>=20161011 order by V1,V2")
re=sqldf("select V1,V2,V7 as V6 from da where V2>=20161001 and V2<=20161031 order by V1,V2")
shop_id=unique(da$V1)
out={}
for (i in 1:length(shop_id)){
tmp=re[which(re$V1==shop_id[i]),]
a=tmp$V6
# a=a+1 #防止出现负数和0 省略
# pre<-stlm(ts(a,frequency = 7),s.window = "periodic",allow.multiplicative.trend = TRUE,robust = T,etsmodel = 'MNN')
pre<-stlm(ts(a,frequency = 7))
# pre=stlf(ts(a,fre=7),t.window=7,s.window='periodic',robust=T)
# fit=stl(ts(a),t.window=7,s.window='periodic',robust=T)
#pre2<-stlf(ts(a,frequency = 7)) robust = T
# pre=forecast(pre,h=14)
# pre=ceiling(pre$mean)
# a=c(as.character(shop_id[i]),pre)
###########使用7天预测
pre=forecast(pre,h=7)
pre=ceiling(pre$mean)
a=c(as.character(shop_id[i]),pre,pre)
##########
# pre=abs(ceiling(pre$mean))
  out=rbind(out,a)
}
out=as.data.frame(out)
# out=sqldf("select * from out order by V1")
out$V1=as.integer(out$V1)
out=sqldf("select * from out order by V1")
#负数变为0
out[which(out$V2<0),]$V2=0
out[which(out$V3<0),]$V3=0
out[which(out$V4<0),]$V4=0
out[which(out$V5<0),]$V5=0
out[which(out$V6<0),]$V6=0
out[which(out$V7<0),]$V7=0
out[which(out$V8<0),]$V8=0
out[which(out$V9<0),]$V9=0
out[which(out$V10<0),]$V10=0
out[which(out$V11<0),]$V11=0
out[which(out$V12<0),]$V12=0
out[which(out$V13<0),]$V13=0
out[which(out$V14<0),]$V14=0
out[which(out$V15<0),]$V15=0

write.table (out, file ="/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/feature/stlf_18_31.txt",sep =",",row.names = F,col.names=F,quote =F)

write.table (out, file ="/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/out/stlf_21_7.csv",sep =",",row.names = F,col.names=F,quote =F)
da<- fread("/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/out/stlf_01_14y.csv",header = FALSE)
re=sqldf("select * from da order by V1")
re=sqldf("select V1,floor(V2),floor(V3),floor(V4),floor(V5),floor(V6),floor(V7),floor(V8),floor(V9),floor(V10),floor(V11),floor(V12),floor(V13),floor(V14),floor(V15) from da order by V1")
write.table (re, file ="/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/out/stlf_01_14_e.csv",sep =",",row.names = F,col.names=F,quote =F)


#融合
options(stringsAsFactors=F,scipen=99)
rm(list=ls());gc()
library(sqldf)
require(data.table)
library(recharts)
d1<- fread("/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/out/0.0802_替换异常_异常.csv",header = FALSE)
d2<- fread("/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/out/LI_20170303_24_2.csv",header = FALSE)
#方法一
re=sqldf("select d1.V1,floor((d1.V2+d2.V2)/2),floor((d1.V3+d2.V3)/2),floor((d1.V4+d2.V4)/2),floor((d1.V5+d2.V5)/2),floor((d1.V6+d2.V6)/2),floor((d1.V7+d2.V7)/2),floor((d1.V8+d2.V8)/2),floor((d1.V9+d2.V9)/2),floor((d1.V10+d2.V10)/2),floor((d1.V11+d2.V11)/2),floor((d1.V12+d2.V12)/2),floor((d1.V13+d2.V13)/2),floor((d1.V14+d2.V14)/2),floor((d1.V15+d2.V15)/2) from d1 left join d2 on d1.V1=d2.V1")
re=sqldf("select d1.V1,floor((0.8*d1.V2+0.2*d2.V2)),floor((0.8*d1.V3+0.2*d2.V3)),floor((0.8*d1.V4+0.2*d2.V4)),floor((0.8*d1.V5+0.2*d2.V5)),floor((0.8*d1.V6+0.2*d2.V6)),floor((0.8*d1.V7+0.2*d2.V7)),floor((0.8*d1.V8+0.2*d2.V8)),floor((0.8*d1.V9+0.2*d2.V9)),floor((0.8*d1.V10+0.2*d2.V10)),floor((0.8*d1.V11+0.2*d2.V11)),floor((0.8*d1.V12+0.2*d2.V12)),floor((0.8*d1.V13+0.2*d2.V13)),floor((0.8*d1.V14+0.2*d2.V14)),floor((0.8*d1.V15+0.2*d2.V15)) from d1 left join d2 on d1.V1=d2.V1")
##方法二
a=0.3
b=0.7
V2=round((a*d1$V2+b*d2$V2))
V3=round((a*d1$V3+b*d2$V3))
V4=round((a*d1$V4+b*d2$V4))
V5=round((a*d1$V5+b*d2$V5))
V6=round((a*d1$V6+b*d2$V6))
V7=round((a*d1$V7+b*d2$V7))
V8=round((a*d1$V8+b*d2$V8))
V9=round((a*d1$V9+b*d2$V9))
V10=round((a*d1$V10+b*d2$V10))
V11=round((a*d1$V11+b*d2$V11))
V12=round((a*d1$V12+b*d2$V12))
V13=round((a*d1$V13+b*d2$V13))
V14=round((a*d1$V14+b*d2$V14))
V15=round((a*d1$V15+b*d2$V15))
re=data.frame(d1$V1,V2,V3,V4,V5,V6,V7,V8,V9,V10,V11,V12,V13,V14,V15)
#方法三
a=0.3
b=0.7
out=data.frame(d1$V1)
d1=as.matrix(d1)
d2=as.matrix(d2)
for(i in 2:15){
    tmp=round((a*d1[,i]+b*d2[,i]))
    out=data.frame(out,tmp)
}
re=as.data.frame(out)

write.table (re, file ="/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/out/790_793_73.csv",sep =",",row.names = F,col.names=F,quote =F)

#按类别分开商户
re=sqldf("select distinct V1,V16,V17,V18 from da ")
library(stringr)
path=c("/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/out/shop_class/")
for(i in 1:length(re$V1)){
tmp=re[i,]
name=str_c(tmp$V16,tmp$V17,tmp$V18,".txt",collapse='')
name=str_replace_all(name,"/","_")
#拼接字符串
pout=str_c(path,name,collapse='')
write.table (tmp$V1, file =pout,sep =",",row.names = F,col.names=F,quote =F,append=TRUE)
}


###构建成提交结果格式
options(stringsAsFactors=F,scipen=99)
rm(list=ls());gc()
library(sqldf)
require(data.table)
library(recharts)
da<- fread("/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/feature/test_re.txt",header = FALSE)
re=sqldf("select  V1,V2,V3 as V4 from da order by V1,V2")
shop_id=unique(re$V1)
out={}
for(i in 1:length(shop_id)){
tmp=re[which(re$V1==shop_id[i]),]
a=ceiling(c(tmp$V4[2:7],tmp$V4[1]))
pre=c(as.character(shop_id[i]),a,a)
out=rbind(out,pre)
}
out=as.data.frame(out)
# out=sqldf("select * from out order by V1")
out$V1=as.integer(out$V1)
out=sqldf("select * from out order by V1")

write.table (out, file ="/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/out/gbdt21_500.csv",sep =",",row.names = F,col.names=F,quote =F)


options(stringsAsFactors=F,scipen=99)
rm(list=ls());gc()
library(sqldf)
require(data.table)
library(recharts)
da<- fread("/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/feature/train_all_weekday.csv",header = FALSE)
#去年双11变化情况
re=sqldf("select * from da where V2>=20151111 and V2<=20151112 order by V1,V2")
shop_id=unique(re$V1)
out={}
for(i in 1:length(shop_id)){
tmp=re[which(re$V1==shop_id[i]),]
a=tmp$V6[1]/tmp$V6[2]
pre=c(as.character(shop_id[i]),a)
out=rbind(out,pre)
}
out=as.data.frame(out)
# out=sqldf("select * from out order by V1")
out$V1=as.integer(out$V1)
out=sqldf("select * from out order by V2 desc")
tmp=out[which(out$V2>2),]
query=sqldf("select * from tmp left join re on tmp.V1=re.V1 and re.V2=20151111")
re=sqldf("select * from da where V2>=20151018 and V2<=20151120 order by V1,V2")
t=query$V1
tmp=out[which(out$V2>1.5&out$V2<=2),]
t2=tmp$V1
pda<- fread("/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/out/0.0793_0.6_0.4.11_0.078902.csv",header = FALSE) #1.5 0.081194  50 92  15 12
for(i in 1:2000){
  if(is.element(i,t)){
    pda[which(pda$V1==i),]
    a=floor(1.5*pda[which(pda$V1==i),]$V12)
    pda[which(pda$V1==i),]$V12=a
  }else if (is.element(i,t2)){
    pda[which(pda$V1==i),]
    a=floor(1.2*pda[which(pda$V1==i),]$V12)
    pda[which(pda$V1==i),]$V12=a
  }
}

for(i in 1:2000){
  if(is.element(i,t)){
    pda[which(pda$V1==i),]
    a=floor(1.03*pda[which(pda$V1==i),]$V11)
    pda[which(pda$V1==i),]$V11=a
  }else if (is.element(i,t2)){
    pda[which(pda$V1==i),]
    a=floor(1.02*pda[which(pda$V1==i),]$V11)
    pda[which(pda$V1==i),]$V11=a
  }
}

pda<- fread("/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/out/0.0793_0.6_0.4.11_0.078902.csv",header = FALSE)
pda<- fread("/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/out/0.08021835.csv",header = FALSE) #0.08019824
re=sqldf("select * from da where V2>=20151011 and V2<=20151031 order by V1,V2")
c1=sqldf("select V1,avg(V6) as V6,V20 from re group by V1,V20 ")
tmp1=c1[which(c1$V20==2),]
tmp1=c1[which(c1$V20==3),]
tmp2=sqldf("select V1,V6 from da where V2=20151110  order by V1")
tmp2=sqldf("select V1,V6 from da where V2=20151111  order by V1")
tmp3=sqldf("select a.V1 as V1,a.V6 as V2,b.V6 as V3 from tmp1 a left join tmp2 b on a.V1=b.V1")
V4=tmp3$V3/tmp3$V2
tmp3=data.frame(tmp3,V4)
tmp4=tmp3[which(V4>1.5&V4<=2),]
t2=tmp4$V1
tmp4=tmp3[which(V4>2),]
t=tmp4$V1
for(i in 1:2000){
  if(is.element(i,t)){
    pda[which(pda$V1==i),]
    a=floor(1.05*pda[which(pda$V1==i),]$V11)
    pda[which(pda$V1==i),]$V11=a
  }else if (is.element(i,t2)){
    pda[which(pda$V1==i),]
    a=floor(1.03*pda[which(pda$V1==i),]$V11)
    pda[which(pda$V1==i),]$V11=a
  }
}


for(i in 1:2000){
  if(is.element(i,t)){
    pda[which(pda$V1==i),]
    a=floor(1.3*pda[which(pda$V1==i),]$V10)
    pda[which(pda$V1==i),]$V10=a
  }else if (is.element(i,t2)){
    pda[which(pda$V1==i),]
    a=floor(1.1*pda[which(pda$V1==i),]$V10)
    pda[which(pda$V1==i),]$V10=a
  }
}
##构建测试集合除去50-92其他都为0
out={}
for(i in 1:2000){
  if(is.element(i,t)){
    # out=rbind(out,pda[which(pda$V1==i),])
  }else if (is.element(i,t2)){
  }else{
    pda[which(pda$V1==i),2:15]=0
  }
}
write.table(pda, file = "/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/out/8021_15_12.csv",sep =",",row.names = F,col.names=F,quote =F)

#查看异常情况 绘图
re=sqldf("select  V1,V2,V6  from da order by V1,V2")
yc=1241

head(da[which(da$V1==yc),],1)
tmp=re[which(re$V1==yc),]
echartr(tmp,as.character(tmp$V2),V6,type = 'line')

fore_value_YC[which(fore_value_YC$V1==yc),2:15]
fore_value_YBX[yc,2:15]

p_update=floor(fore_value_YC[which(fore_value_YC$V1==yc),2:15]*1.3)

write.table (p_update, file ="/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/post_20170225_16_3/tmp_update.txt",sep =",",row.names = F,col.names=F,quote =F)



