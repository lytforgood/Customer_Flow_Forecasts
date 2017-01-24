#时序模型
options(stringsAsFactors=F,scipen=99)
rm(list=ls());gc()
library(sqldf)
require(data.table)
library(recharts)
da<- fread("/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/feature/train_all.txt",header = FALSE)
#测试集选择的 20161018-20161031

#1.前两周的情况 --20161004-20161017  含国庆 应该不准  应该含有空缺值 补0(python已做)
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

#2.前两周均值
avg_re=sqldf("select V1,avg(V6) as r1 from da where V2>=20161004 and V2<=20161017 group by V1")
shop_id=unique(avg_re$V1)
out={}
for (i in 1:length(shop_id)){
tmp=avg_re[which(avg_re$V1==shop_id[i]),]
a=c(as.character(shop_id[i]),rep(tmp$r1,14))
out=rbind(out,a)
}
write.table (out, file ="/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/feature/twoavg_18_31.txt",sep =",",row.names = F,col.names=F,quote =F)

#3.三阶指数平滑  选取前1个月的进行训练
re=sqldf("select V1,V2,V6 from da where V2>=20160919 and V2<=20161017 order by V1,V2")
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


#4.stl分解-以鲁棒局部加权回归作为平滑方法的时间序列分解方法
library(forecast)
re=sqldf("select V1,V2,V6 from da where V2>=20160919 and V2<=20161017 order by V1,V2")
shop_id=unique(da$V1)
out={}
for (i in 1:length(shop_id)){
tmp=re[which(re$V1==shop_id[i]),]
a=tmp$V6
a=a+1 #防止出现负数和0
# pre<-stlm(ts(a,frequency = 7),s.window = "periodic",allow.multiplicative.trend = TRUE,robust = T,etsmodel = 'MNN')
pre<-stlm(ts(a,frequency = 7))
# pre=stlf(ts(a,fre=7),t.window=7,s.window='periodic',robust=T)
# fit=stl(ts(a),t.window=7,s.window='periodic',robust=T)
#pre2<-stlf(ts(a,frequency = 7)) robust = T
pre=forecast(pre,h=14)
pre=pre$mean
a=c(as.character(shop_id[i]),pre)
  out=rbind(out,a)
  }
write.table (out, file ="/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/feature/stlf_18_31.txt",sep =",",row.names = F,col.names=F,quote =F)

