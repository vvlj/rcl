from pretreatment.get_alarm import AlarmInfo
from pretreatment.topology import get_topology_node_edge_dct
import datetime
import numpy as np
import pandas as pd


def draw_from_root(alarm_data):
    """从根节点出发，看传播特征
    :param : alarm_data
    :return:
    """


def round_time(ts, delta):
    """时间向下取整"""
    t = datetime.datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
    return str(t - datetime.timedelta(seconds=t.second % delta))


# 原数据 -> 每个时段数据-> 多个拓扑图
def get_time_data(ith, delta):
    """
    :return:
    """
    ainfo = AlarmInfo()
    alarm_info = ainfo.get_alarm_info_tmp(ith)
    # 1. 时间段向下取整
    alarm_info['time'] = alarm_info['time'].apply(round_time, delta=delta)
    # 2. 分组
    for t, group in alarm_info.groupby('time'):
        yield t, group


def get_time_freq_feature(ith, delta):
    """获取每段时间出现告警数量的平吕
    :param ith:
    :param delta:
    :return:
    """
    return [len(group) for t, group in get_time_data(ith, delta)]


# 构造时间维度特征：
def get_time_feature(ith, delta=30, filtering=True):
    ainfo = AlarmInfo()
    alarm_info = ainfo.get_alarm_info_tmp(ith)
    # 1. 时间段向下取整
    alarm_info['time'] = alarm_info['time'].apply(round_time, delta=delta)
    # 2. 筛选出频次高的
    if filtering:
        freqs = alarm_info['node_name'].value_counts()
        node_set = freqs[(freqs >= freqs.describe()['25%'] * 1.5)].index  # 筛选频率高于下4分位的节点
    else:
        node_set = alarm_info['node_name'].unique()
    node_index_dct = dict(zip(node_set, range(len(node_set))))
    time_feature = np.zeros((len(alarm_info['time'].unique()), len(node_set)), dtype=int)
    for i, (t, group) in enumerate(alarm_info.groupby('time')):
        # time_feature[i, :] = time_feature[i-1, :]  # 保留
        for node in group['node_name']:
            if node in node_index_dct:
                # time_feature[i, node_index_dct[node]] += 1
                time_feature[i, node_index_dct[node]] = 1
    if sum(alarm_info['is_root']):
        root = node_index_dct[alarm_info[alarm_info['is_root'] == 1]['node_name'].values[0]]
    else:
        root = None
    return root, time_feature


class FeatureEn:
    def __init__(self):
        self.ainfo = AlarmInfo()
        self.edge_set = set()
        for node, to_nodes in get_topology_node_edge_dct().items():
            for to_node in to_nodes:
                self.edge_set.add((int(node[5:]), int(to_node[5:])))
                self.edge_set.add((int(to_node[5:]), int(node[5:])))

    def get_time_feature(self, ith, delta=30, filtering=True):
        # edge_lst = []
        # node_lst = []
        alarm_info = self.ainfo.get_alarm_info_tmp(ith)
        node_index_dct = {}
        for i, node in enumerate(set(alarm_info['node_name'])):
            node_index_dct[node] = i
        # 1. 时间段向下取整
        alarm_info['time'] = alarm_info['time'].apply(round_time, delta=delta)
        time_feature = np.zeros((len(alarm_info['time'].unique()), len(set(alarm_info['node_name']))), dtype=int)
        for i, (t, group) in enumerate(alarm_info.groupby('time')):
            nodes = set(group['node_name'])  # 不考虑重复
            if filtering:
                while nodes:
                    cur_node = nodes.pop()
                    for next_node in nodes:
                        if (cur_node, next_node) in self.edge_set:
                            time_feature[i, node_index_dct[cur_node]] += 1
                            time_feature[i, node_index_dct[next_node]] += 1
            else:
                for node in nodes:
                    time_feature[i, node_index_dct[node]] = 1
        if sum(alarm_info['is_root']):
            root = node_index_dct[alarm_info[alarm_info['is_root'] == 1]['node_name'].values[0]]
        else:
            root = None
        print(root)
        return pd.DataFrame(time_feature, columns=node_index_dct.keys()), root
