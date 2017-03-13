#绘图
options(stringsAsFactors=F,scipen=99)
rm(list=ls());gc()
library(sqldf)
require(data.table)
library(recharts)
library('htmlwidgets') ##保持echarts文件为html

da<- fread("/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/feature/train_all.txt",header = FALSE)
#测试集选择的 20161018-20161031
re=sqldf("select V1,V2,V6 from da where V2>=20160901 and V2<=20161031 order by V1,V2")
shop_id=unique(da$V1)

for (i in 1:length(shop_id)){

tmp=re[which(re$V1==shop_id[i]),]
echartr(tmp,as.character(tmp$V2),V6,type = 'line')


}

# pic=echartr(d_huo,as.character(d_huo$start), n1,type = 'line') %>% setSymbols('emptycircle') %>% addMarkLine(data=data.frame(type='average', name1='Avg')) %>% addMarkPoint(series=1, data=data.frame(type='max', name='Max')) %>% setTitle('20160730-20161028活跃用户变化情况',paste0(''),textStyle=list(color='red')) %>% setYAxis(min=800)
# saveWidget(pic,"/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/feature/pic.html")
