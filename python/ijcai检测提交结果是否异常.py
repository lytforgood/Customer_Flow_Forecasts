# -*- coding: utf-8 -*-
#检测提交结果是否异常
def inspect(url):
    import pandas as pd
    import numpy as np

    data = pd.read_csv(url,header=None)
    result = data
    flag = True
    if data.shape != (2000,15):
        print '数据缺失或多余！请重新检查。'
        flag = False
    if data.abs().sum().sum() != data.sum().sum():
        print '结果中出现负数！已用0代替。'
        result = data - data[data < 0].fillna(0)
        flag = False
    for tp in data.dtypes.values:
        if tp.type is not np.int64:
            print '数据不是整数！已替换为整数。'
            flag = False
            break
    if True in (data.isnull().values):
        print '数据中包含空值，已替换为零。'
    result = result.fillna(0).astype(int)
    if flag == True:
        print 'Great！数据完整，不存在空值、负数和零。'

    return result

inspect("../../data/dataset/out/融合_50x15.csv")
