from featuer.spread import SpreadNetwork
import pandas as pd
from pretreatment.feat_en import FeatureEn
max_rank = 15
time_window = 5


class RootLocation:
    def __init__(self):
        pass

    def fix(self, i):
        pass

    def predict(self, i, flag='test'):
        snw = SpreadNetwork(i, flag)
        cost_dct = snw.get_cost_dct(12, True)
        # 合并后比较
        if flag == 'test':
            time_feature = FeatureEn(flag).get_time_feature(i, time_window, False)
        else:
            time_feature = FeatureEn(flag).get_time_feature(i, time_window, False)[0]
        corr = abs(time_feature.corr()).sum()
        bind_lst = []
        for node, cost in cost_dct.items():
            bind_lst.append([node, cost + corr[node]])  # 四则运算试试
        bind_df = pd.DataFrame(bind_lst, columns=['node', 'cost'])
        bind_df.sort_values('cost', ascending=False, inplace=True)
        nodes = set(bind_df['node'][:max_rank])
        edges = []
        for node in nodes:
            edges.extend((node, adjoin) for adjoin in set(snw.node_edge_dct[node]) & nodes)
        snw.draw(list(nodes), edges)
        return nodes, edges, bind_df['node'].iloc[0]

    def _get_root(self):
        pass


rl = RootLocation()
snw, nodes, bind_df = rl.predict(0)
