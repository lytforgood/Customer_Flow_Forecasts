Customer Flow Forecasts on Koubei.com
==
IJCAI 2017 Competition
背景 Background
随着移动定位服务的流行，阿里巴巴和蚂蚁金服逐渐积累了来自用户和商家的海量线上线下交易数据。蚂蚁金服的O2O平台“口碑”用这些数据为商家提供了包括交易统计，销售分析和销售建议等定制的后端商业智能服务。举例来说，口碑致力于为每个商家提供销售预测。基于预测结果，商家可以优化运营，降低成本，并改善用户体验。

scala数据预处理
====
1. DateFormat 时间处理函数工具类
2. DateTransform 转换数据时间
3. DataSQL 执行sql查询
4. querySql 统计量生成

R统计分析 时序模型
====
1. time.R 时间序列模型
2. WNN.R  Weighted Nearest Neighbors模型
参考:Electricity Market Price Forecasting Based on Weighted Nearest Neighbors Techniques

python特征提取 训练模型
====
IJCAI.ipynb python使用记录

1. union.py 原始数据整合
2. preprocessing.py 数据预处理 + 特征变换
3. Evaluate_detail.py 评价函数
   Evaluate.py 测试集构建填充缺失值+评价函数
4. test_build.py 构建测试集时间等特征
5. feature.py 特征提取+模型训练
6. baseline.py 星期特征baseline

java
====
Evaluate.java 评测函数
