from pyecharts import options as opts
from pyecharts.charts import Graph, Page


def draw_topology(nodes, links):
    """
    画拓扑图
    :param nodes: [{"name": "结点1", "symbolSize": 10},]
    :param links: [{"source": "结点1", "target": 结点2},]
    :return:
    """
    c = (
        Graph()
        .add("", nodes, links, repulsion=8000)
        .set_global_opts(title_opts=opts.TitleOpts(title="Graph-基本示例"))
    )
    return c


def draw_topology_test():
    nodes = [
        {"name": "结点1", "symbolSize": 10},
        {"name": "结点2", "symbolSize": 20},
        {"name": "结点3", "symbolSize": 30},
        {"name": "结点4", "symbolSize": 40},
        {"name": "结点5", "symbolSize": 50},
        {"name": "结点6", "symbolSize": 40},
        {"name": "结点7", "symbolSize": 30},
        {"name": "结点8", "symbolSize": 20},
    ]
    links = []
    for i in nodes:
        for j in nodes:
            links.append({"source": i.get("name"), "target": j.get("name")})
    draw_topology(nodes, links).render('./data/graph.html')

