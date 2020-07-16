from featuer.spread import SpreadNetwork
from myfunc.matplot import *
import seaborn as sns
from sklearn.cluster import DBSCAN
import numpy as np
import pandas as pd

# for i in range(100):
#     try:
#         snw = SpreadNetwork(i)
#         cost_dct = snw.get_cost_dct(2, True)
#         cost_df = pd.DataFrame(cost_dct.items(), columns=['node', 'cost'])
#         nodes = set(cost_df['node'][cost_df['cost'] > cost_df['cost'].describe()['75%']])
#         # edges = []
#         # for node in nodes:
#             # edges.extend((node, adjoin) for adjoin in set(snw.node_edge_dct[node]) & nodes)
#         # snw.draw(list(nodes), edges)
#
#         # 分类特征
#         # sns.distplot(list(cost_dct.values()))
#         # plt.title(f'{i}_{str(snw.root)}')
#         # plt.savefig(f'./data/eda/cost_weight_{i}.png')
#         # plt.show()
#     except ValueError:
#         print(i)


# 根因节点的特性：传播路径长，出现时间早， 试试二分法
#
# snw = SpreadNetwork(0)
# cost_dct = snw.get_cost_dct(2, True)


# 最大跳数选择
def max_jump_select():
    snw_lst = []
    for i in range(100):
        snw_lst.append(SpreadNetwork(i))
    total_rank_lst = []
    for max_jump in range(100):
        total_rank = 0
        for i in range(100):
            snw = snw_lst[i]
            if snw.root is None:
                continue
            cost_dct = snw.get_cost_dct(max_jump, True)
            cost_df = pd.DataFrame(cost_dct.items(), columns=['node', 'cost'])
            cost_df.sort_values('cost', inplace=True, ascending=False)
            total_rank += list(cost_df['node']).index(snw.root)
        total_rank_lst.append(total_rank)
    min_ = min(total_rank_lst)
    print(min_)
    return total_rank_lst.index(min_)


# a = max_jump_select()； print(a)
rank_lst = []
for i in range(100):
    snw = SpreadNetwork(i)
    if snw.root is None:
        continue
    cost_dct = snw.get_cost_dct(12, True)
    cost_df = pd.DataFrame(cost_dct.items(), columns=['node', 'cost'])
    cost_df.sort_values('cost', inplace=True, ascending=False)
    rank_lst.append([cost_df[cost_df['node']==snw.root]['cost'].values[0], list(cost_df['node']).index(snw.root), snw.reason])
    # rank = list(cost_df['node']).index(snw.root)
    # if rank < 5:
    #     nodes = set(cost_df['node'][:20])
    #     edges = []
    #     for node in nodes:
    #         edges.extend((node, adjoin) for adjoin in set(snw.node_edge_dct[node]) & nodes)
    #     snw.draw(list(nodes), edges)
    #     input()
a = pd.DataFrame(rank_lst).sort_values(1)
