from featuer.spread import SpreadNetwork
import seaborn as sns
import pandas as pd
from pretreatment.feat_en import FeatureEn
import matplotlib.pyplot as plt

# 用来正常显示中文标签，SimHei是字体名称，字体必须再系统中存在，字体的查看方式和安装第三部分
plt.rcParams['font.sans-serif']=['SimHei']
# 用来正常显示负号
plt.rcParams['axes.unicode_minus']=False
fe = FeatureEn()


def draw_cost_distribution():
    """绘画损失分布图： 依据分布图特征，可能可以用于异常过滤"""
    for i in range(100):
        snw = SpreadNetwork(i)
        cost_dct = snw.get_cost_dct(12, True)
        # 分类特征
        sns.distplot(list(cost_dct.values()))
        plt.title(f'{i}_{str(snw.root)}')
        plt.savefig(f'./data/eda/cost_weight_{i}.png')
        plt.show()


# 最大跳数选择
def max_jump_select():
    """
    :return: 最终跳数是选择  12
    """
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


# 探究传播特征 = 时间关联特征 + 空间拓扑特征？
def explore_spread_feture():
    """
    :return:  时间关联特征 + 空间拓扑特征 是否比单独更优？
    """
    rank_lst = []
    for i in range(100):
        snw = SpreadNetwork(i)
        if snw.root is None:
            continue
        cost_dct = snw.get_cost_dct(12, True)  # 空间拓扑特征
        time_feature, root = fe.get_time_feature(i, 5, False)  # 时间关联特征
        corr = abs(time_feature.corr()).sum()
        # 合并后比较
        bind_lst = []
        for node, cost in cost_dct.items():
            bind_lst.append([node, cost + corr[node]])  # 四则运算试试
        corr.sort_values(ascending=False, inplace=True)
        cost_sort = sorted(cost_dct, key=lambda x: cost_dct[x], reverse=True)
        rank_lst.append([list(corr.index).index(root), cost_sort.index(root), list(pd.DataFrame(bind_lst).sort_values(1, ascending=False)[0]).index(root)])
    total_rank_df = pd.DataFrame(rank_lst)
    print("排名之和为：", sum(total_rank_df[2]))
    return total_rank_df


# 合并（时间关联特征与空间拓扑特征）的传播图
def draw_combind_spread(num=15):
    """
    :param num: 最节点/排名数
    :return:
    """
    for i in range(100):
        snw = SpreadNetwork(i)
        if snw.root is None:
            continue
        cost_dct = snw.get_cost_dct(12, True)
        # 合并后比较
        time_feature = fe.get_time_feature(i, 5, False)[0]
        corr = abs(time_feature.corr()).sum()
        bind_lst = []
        for node, cost in cost_dct.items():
            bind_lst.append([node, cost + corr[node]])  # 四则运算试试
        bind_df = pd.DataFrame(bind_lst, columns=['node', 'cost'])
        bind_df.sort_values('cost', ascending=False, inplace=True)
        if snw.root in bind_df['node'][:num].values:
            nodes = set(bind_df['node'][:num])
            edges = []
            for node in nodes:
                edges.extend((node, adjoin) for adjoin in set(snw.node_edge_dct[node]) & nodes)
            snw.draw(list(nodes), edges)


if __name__ == '__main__':
    # draw_cost_distribution()  # 损失分布图
    explore_spread_feture()
    draw_combind_spread()
    # a = max_jump_select(); print(a)
