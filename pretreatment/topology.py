from pyecharts import options as opts
from pyecharts.charts import Graph, Page
import json
from pretreatment.get_alarm import AlarmInfo


topology_dir = './data/topology/'
label_opts = opts.LabelOpts(False)


def _get_topology(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


def get_topology_sys_nodes_dct():
    """
    提取系统和节点从属关系
    return: {sys: [node1, node2]}
    """

    return _get_topology(topology_dir + 'sys_and_nodes.json')


def get_topology_sys_edge_dct():
    """
        提取系统的边集
        return: {sys1: [sys2, sys3]}
    """
    return _get_topology(topology_dir + 'topology_edges_sys.json')


def get_topology_node_edge_dct():
    """
    提取节点的边集
    return {node1: [node2, node3]}
    """
    return _get_topology(topology_dir + 'topology_edges_node.json')


def dump_node_edge_second_level():
    topology_node_edge = get_topology_node_edge_dct()
    second_level = {}
    for node, adjoins in topology_node_edge.items():
        second_adjoins = set()
        for next_node in adjoins:
            second_adjoins.update(set(topology_node_edge[next_node]))
        second_level[node] = {'first': adjoins, 'second': list(second_adjoins)}
    with open(topology_dir + 'second_level.json', 'w') as f:
        json.dump(second_level, f)


def get_node_edge_second_level():
    return _get_topology(topology_dir + 'second_level.json')


def draw_topology(nodes, edges, name='', categories=None, root=None):
    """
    画拓扑图，传入具有告警的节点
    :param nodes: [{"name": "结点1", "symbolSize": 10},]
    :param edges: [{"source": "结点1", "target": 结点2},]
    :param name
    :param categories
    :param root
    :return:
    """
    if not isinstance(nodes, dict):
        node_lst = []
        for node in nodes:
            if node == root:
                node_lst.append({'name': node, 'symbolSize': 20})  # , 'label_opts': label_opts})
            else:
                node_lst.append({'name': node, 'symbolSize': 10})  # , 'label_opts': label_opts})
        edge_lst = []
        for node, target in edges:
            edge_lst.append({'source': node, 'target': target})
        nodes = node_lst
        edges = edge_lst
    (
        Graph()
            .add("", nodes, edges, categories=categories, repulsion=8000)
            # .set_global_opts(title_opts=opts.TitleOpts(title=f"Graph-{sum(root_index)}"))
            # .set_series_opts(label_opts=label_opts)
    ).render(f'./data/graph_{name}.html')


def draw_topology_local(alarm_info, name=''):
    """
    画拓扑图，传入具有告警的节点，
    :param alarm_info: [{"name": "节点1", ""}]
    :param name: [{"name": "节点1", ""}]
    :return:
    """
    # 设置局部拓扑图
    sys_set = alarm_info['sysEname'].unique()
    sys_nodes_dct = get_topology_sys_nodes_dct()
    nodes, edges, categories = [], [], []
    node_edge = get_topology_node_edge_dct()
    node_index_dct = {}  # 存放节点所在列表的索引，方便查找
    for i, sys in enumerate(sys_set):
        sys = 'SYS_' + str(sys)
        categories.append({'name': sys})
        for node in sys_nodes_dct[sys]:
            nodes.append({'name': node, 'symbolSize': 10, 'category': i, 'label_opts': label_opts})  # , 'color': 1})
            node_index_dct[node] = len(nodes) - 1
            for target in node_edge[node]:
                edges.append({'source': node, 'target': target})
    # 读取告警节点数据
    for node in alarm_info['node_name']:
        nodes[node_index_dct['node_' + str(node)]]['symbolSize'] = 40
    # 设置根因节点
    root_index = alarm_info['is_root'] == 1
    if sum(root_index):
        root_node = alarm_info[root_index]['node_name'].iloc[0]
        nodes[node_index_dct['node_' + str(root_node)]]['symbolSize'] = 60
    draw_topology(nodes, edges, name, categories)


def draw_topology_test():
    # sys_set = ['SYS_1', 'SYS_7']
    sys_nodes_dct = get_topology_sys_nodes_dct()
    sys_set = sys_nodes_dct.keys()
    nodes, edges, categories = [], [], []
    node_edge = get_topology_node_edge_dct()
    for i, sys in enumerate(sys_set):
        categories.append({'name': sys})
        for node in sys_nodes_dct[sys]:
            nodes.append({'name': node, 'symbolSize': 10, 'category': i})  # , 'color': 1})
            for target in node_edge[node]:
                edges.append({'source': node, 'target': target})
    (
        Graph()
            .add("", nodes, edges, categories=categories, repulsion=8000)
            .set_global_opts(title_opts=opts.TitleOpts(title="Graph-基本示例"))
    ).render('./data/graph.html')
