from pretreatment.topology import draw_topology_test
from pretreatment.get_alarm import alarm_info

draw_topology_test()
ainfo = alarm_info()
# 更新训练集
ainfo.add_feature()
# 对告警信息进行分类和存储
ainfo.get_alarm_type()
ainfo.get_alarm_info()