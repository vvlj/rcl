from pretreatment.get_alarm import AlarmInfo
from pretreatment.feat_en import FeatureEn
import matplotlib.pyplot as plt
import pandas as pd


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


def get_first_time_dct(i):
    aifo = AlarmInfo()
    info_df = aifo.get_alarm_info_tmp(i)
    first_time_dct = {}
    info_df['time'] = pd.to_datetime(info_df['time'])
    min_date = info_df['time'].min()
    for _, raw in info_df.iterrows():
        if raw['node_name'] not in first_time_dct:
            first_time_dct[raw['node_name']] = (raw['time'] - min_date).seconds
    return first_time_dct


def draw_time_scatter(i):
    aifo = AlarmInfo()
    info_df = aifo.get_alarm_info_tmp(i)
    first_time_dct = {}
    info_df['time'] = pd.to_datetime(info_df['time'])
    min_date = info_df['time'].min()
    for _, raw in info_df.iterrows():
        if raw['node_name'] not in first_time_dct:
            first_time_dct[raw['node_name']] = (raw['time'] - min_date).seconds
    plt.scatter(first_time_dct.values(), first_time_dct.keys(), s=10)
    if sum(info_df['is_root']):
        root = info_df[info_df['is_root'] == 1]['node_name'].values[0]
        plt.scatter([first_time_dct[root]], [root], s=100)
        plt.title(f"{i}:有根因")
    else:
        plt.title(f"{i}:无根因")
    plt.savefig(f'./data/eda/time_scatter_{i}.png')
    plt.show()


def draw_time_scatter_test():
    for i in range(100):
        draw_time_scatter(i)


if __name__ == '__main__':
    draw_time_feature(0)
    draw_time_scatter_test()  # 第一次出现的时间散点图
