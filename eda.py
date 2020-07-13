from pretreatment.topology import draw_topology_test, draw_topology_local, draw_topology
from pretreatment.get_alarm import preporcess, AlarmInfo
from pretreatment.feat_en import get_time_data, get_time_feature, get_time_freq_feature, FeatureEn
import matplotlib.pyplot as plt
import pandas as pd
from myfunc.matplot import *
import seaborn as sns


# 传播拓扑图， 单位时间绘制一次
def draw_time_feature(i):
    # 获取数据
    featen = FeatureEn()
    time_feature, root = featen.get_time_feature(i, 10, False)
    for i in range(len(time_feature)):
        raw = time_feature.iloc[i]
        nodes = list(raw[raw > 0].index)
        while nodes:
            cur_node = nodes.pop()
            for next_node in nodes:
                if (cur_node, next_node) in featen.edge_set:
                    pass



    # featen.=

    # 获取邻接表
    # 构建新数据
    # 画图
draw_time_feature(0)