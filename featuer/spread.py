from pretreatment.get_alarm import AlarmInfo
from pretreatment.my_network import Network
from pretreatment.topology import get_topology_node_edge_dct
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

# 用来正常显示中文标签，SimHei是字体名称，字体必须再系统中存在，字体的查看方式和安装第三部分
plt.rcParams['font.sans-serif']=['SimHei']
# 用来正常显示负号
plt.rcParams['axes.unicode_minus']=False


# 构建传播图
class SpreadNetwork(Network):
    """一个数据集，一个传播图"""
    def __init__(self, i, max_time=None):
        """
        :param i:
        :param max_time: 单位是秒
        """
        self.i = i
        super().__init__()
        # 1. 每个节点的最早出现时间
        info_df = AlarmInfo().get_alarm_info_tmp(i)
        if sum(info_df['is_root']):
            self.root, self.reason = info_df[info_df['is_root'] == 1][['node_name', 'trigger']].values[0]
        else:
            self.root, self.reason = None, None
        first_time_dct = {}
        info_df['time'] = pd.to_datetime(info_df['time'])
        min_date = info_df['time'].min()
        max_time = (info_df['time'].max() - min_date).seconds if max_time is None else max_time
        for _, raw in info_df.iterrows():
            if raw['node_name'] not in first_time_dct:
                ts = (raw['time'] - min_date).seconds
                if ts > max_time:
                    break
                first_time_dct[raw['node_name']] = ts
        self.node_weight_dct = first_time_dct
        # 2. 构建图
        topology_node_edge_dct = {}
        for key, items in get_topology_node_edge_dct().items():  # node对应不上，需变换
            topology_node_edge_dct[int(key[5:])] = set(int(i[5:]) for i in items)
        self.nodes = list(first_time_dct.keys())
        for node in self.nodes:
            edge_lst = []
            adjoin_lst = topology_node_edge_dct[node] & (set(self.nodes) ^ {node})
            for adjoin in adjoin_lst:
                edge_lst.append((node, adjoin))
                self.edge_weight_dct[(node, adjoin)] = first_time_dct[adjoin] - node  # 考虑是否取绝对值
            self.node_edge_dct[node] = adjoin_lst
            self.edges.extend(edge_lst)

    def get_cost_by_node(self, node, max_jump=1e2, weight=True):
        """从一个根结点出发，查看传播特征"""
        cost = 0
        num = 0
        cur_jump = 0
        visited = set()
        to_visited_stack = [node]
        while to_visited_stack and cur_jump < max_jump:
            cur = to_visited_stack.pop()
            for adjoin in self.node_edge_dct[cur]:
                if adjoin not in visited:
                    visited.add(adjoin)
                    cost += self.edge_weight_dct[(cur, adjoin)]
                    to_visited_stack.append(adjoin)
                    num += 1
            cur_jump += 1
        if num == 0:
            return 0
        else:
            # return cost / num / (self.node_weight_dct[node] + 1) if weight else cost / num
            return cost / (self.node_weight_dct[node] + 1) /cur_jump if weight else cost

    def get_cost_dct(self, max_jump=1e2, weight=True):
        return dict((node, self.get_cost_by_node(node, max_jump, weight)) for node in self.nodes)

    def draw(self, nodes, edges):
        mg = nx.MultiGraph()
        mg.add_nodes_from(nodes)
        mg.add_edges_from(edges)
        if self.root is None:
            nx.draw(mg, with_labels=True)
        else:
            node_color = ['blue'] * len(nodes)
            node_color[nodes.index(self.root)] = 'red'
            nx.draw(mg, with_labels=True, node_color=node_color)
        plt.savefig(f'./data/eda/spread_net{self.i}.png')
        plt.show()

    def small_network(self, nodes):
        to_del = set(self.nodes) ^ set(nodes)
        for node in to_del:
            self.nodes.remove(node)
            adjoin_lst = self.node_edge_dct[node] & (to_del ^ {node})
            for adjoin in adjoin_lst:
                self.edges.remove((node, adjoin))
                del self.edge_weight_dct[(node, adjoin)]
            del self.node_edge_dct[node]
            del self.node_weight_dct[node]
