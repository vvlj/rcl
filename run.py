from pretreatment.topology import draw_topology_test, draw_topology_local, draw_topology, get_topology_node_edge_dct
from pretreatment.get_alarm import preporcess, AlarmInfo
from pretreatment.feat_en import get_time_data, get_time_feature, get_time_freq_feature
import matplotlib.pyplot as plt
import pandas as pd
from myfunc.matplot import *
import seaborn as sns

# 用来正常显示中文标签，SimHei是字体名称，字体必须再系统中存在，字体的查看方式和安装第三部分
plt.rcParams['font.sans-serif']=['SimHei']
# 用来正常显示负号
plt.rcParams['axes.unicode_minus']=False


train_path_lst = range(100)  # 预处理后的数据位置
ainfo = AlarmInfo()

# preporcess()  # 预处理
# draw_topology_local(0)

# 频率分布图；不同数据集告警频率的分布是相似的吗？...节点间的调用链难以识别，根因必定是根节点
# node_feq_dct = {}
# for i in train_path_lst:
#     data = ainfo.get_alarm_info_tmp(i)
#     print(data['is_root'].sum())
#     if data['is_root'].sum():
#         continue
#     for freq in data['node_name'].value_counts():
#         freq_key = int(freq / 5)
#         node_feq_dct[freq_key] = node_feq_dct.get(freq_key, 0) + 1
# plt.scatter(node_feq_dct.keys(), node_feq_dct.values())
# plt.show()
# print(node_feq_dct)


# 算法步骤：
# 1 构建训练集
# 2. 推因果图
# 3. 因果图推根因？？？  根因与因果图的关系？？


# 根因有何特性？？
ith = 0
# data = ainfo.get_alarm_info_tmp(ith)
# node_lst = data['node_name'].unique()
# for i, (t, group) in enumerate(get_time_data(ith)):
#     print(group)
#     draw_topology_local(group, i)



# 1:9
# 2:6
# 3:4
# 4:3
# 5:4
# 6:3
# 7:2
# 8:1
# 9:8
# 10:4
# 11:8
# 12:7
# 13: 6(x)
# 14: 4
# 15: 6
# 时间维度，因果图推理
from pcalg import estimate_skeleton, estimate_cpdag
from gsq.ci_tests import ci_test_dis
# for i in range(3, 7):
#     print(i)
# alpha区间[0.17, 0.32]， 暂定0.25
# delta区间[3, 7]
# for i in range(100):
#     print(i, end='\t')
#     if i == 17:
#         continue
#     root, time_feature = get_time_feature(i, 5, filtering=False)
#
#     print(root)
#     (g, sep_set) = estimate_skeleton(indep_test_func=ci_test_dis, data_matrix=time_feature, alpha=0.2)
#     g = estimate_cpdag(skel_graph=g, sep_set=sep_set)
#     draw_topology(g.nodes, g.edges, name=str(i), root=root)
#

from pretreatment.feat_en import FeatureEn

fe = FeatureEn()
# time_feature, node = fe.get_time_feature(0, 5, False)
# (g, sep_set) = estimate_skeleton(indep_test_func=ci_test_dis, data_matrix=time_feature, alpha=0.2)
# g = estimate_cpdag(skel_graph=g, sep_set=sep_set)
# draw_topology(g.nodes, g.edges, root=node)

for i in range(100):
    if i == 17:
        continue

    time_feature, node = fe.get_time_feature(i, 5, False)
    plt.title(str(node))
    sns.distplot(abs(time_feature.corr()).sum())
    plt.savefig(f'{i}.png')
    plt.show()

# time_feature, node = fe.get_time_feature(0, 5, False)
# a = abs(time_feature.corr()).sum()
# b = a[a > a.describe()['75%']].index