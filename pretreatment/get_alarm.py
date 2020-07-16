import pandas as pd
from sklearn.preprocessing import LabelEncoder
import re

path_dct = {'test': './data/test/%d',
            'train': './data/train/%d',
            "new_train": './data/new_train/%d',
            "new_test": './data/new_train/%d',
            'node_list': [list(range(0, 100)), list(range(0, 20))]}


class AlarmInfo(object):
    def __init__(self, flag="train"):
        self.alarm_type = {}
        self.alarm_list = []
        self.flag = flag
        self.train = None
        self.label_list = None
        self.label = LabelEncoder()
        self.name = []
        self.trigger = []
        self.alarm_info = []

    def add_feature(self):
        """
        对数据进行特征处理,并改写数据集
        :return:
        """
        for j in path_dct["node_list"][self.flag == 'test']:
            self.train = pd.read_csv(path_dct[self.flag] % j + ".csv", encoding="utf-8")
            for i in self.train["triggername"].tolist():
                self.name.append(i.split(" ", 1)[0])

                self.trigger.append(i.split(" ", 1)[1])

            self.train["node_name"] = self.name
            self.train["trigger"] = self.trigger
            self.train["trigger"].replace({r'url:(.*)访问失败': 'url访问失败',
                                           r'FullGC次数(.*)': 'FullGC次数大于阈值',
                                           r'FullGC平均耗时(.*)': 'FullGC平均耗时大于阈值',
                                           '上I/O等待负载(.*)': 'I/O等待负载过大',
                                           r'(.*)慢响应(.*)': '网页响应慢',
                                           r'硬盘Slot [0, 9]\d{1,2}状态为Failed': '硬盘状态failed',
                                           'Nginx 80端口的连接数大于2000': 'Nginx端口连接数过大',
                                           '上CPU Steal Time持续5分钟超过10%': 'CPU Steal Time持续过高',
                                           r'堆内存平均使用率(.*)': '堆内存平均使用率大于阈值',
                                           'JBOSS 8080端口的连接数大于400': 'JBOSS 8080端口连接数过大',
                                           '网卡eth0(.*)': '网卡接收/发出流量过大',
                                           '(.*)请求延时大于5分钟': '请求延时过大',
                                           '网卡流量unknown': '网卡流量未知',
                                           '空闲交换空间小于50%': '空闲交换空间过小',
                                           r'端口(.*)通信异常': '端口通信异常',
                                           r'空闲CPU为(.*)': '空闲CPU空间持续过小',
                                           r'日志(.*)': '日志包含错误信息',
                                           'sdd IO使用率持续30分钟大于90%': 'sdd IO使用率持续过高',
                                           'sdb IO使用率持续30分钟大于90%': 'sdd IO使用率持续过高',
                                           r'ping丢包率(.*)': 'ping丢包严重',
                                           'ping延迟时间持续3分钟大于100ms': 'ping延迟时间长'}, regex=True, inplace=True)
            self.train.drop(["triggername"], axis=1, inplace=True)
            self.coding()
            if self.flag == 'train':
                self.train.to_csv(f"./data/new_train/{j}.csv", encoding="utf-8", index=False)
            else:
                self.train.to_csv(f"./data/new_test/{j}.csv", encoding="utf-8", index=False)
            self.name = []
            self.trigger = []

    def coding(self):
        """
        特征编码
        :return:
        """
        self.train["sysEname"] = [int(i[4:]) for i in self.train["sysEname"]]
        self.train["node_name"] = [int(i[7:]) for i in self.train["node_name"]]
        # self.train["trigger"] = self.label.fit_transform(self.train["trigger"])
        # self.label_list = dict(zip(list(range(0, len(self.label.classes_))), self.label.classes_))
        # self.train["time"] = [i[-5:] for i in self.train["time"]]

    def get_alarm_type(self):
        """
        对告警信息进行分词、过滤、提取关键信息并编号
        :return: {label:告警信息类型}
        """
        for i in path_dct["node_list"][self.flag == 'test']:
            for j in pd.read_csv(path_dct[self.flag] % i + ".csv", encoding="utf-8")["triggername"]:
                self.alarm_info.append(j.split(" ", 1)[1])
        df = pd.DataFrame(self.alarm_info)
        df[0].replace({r'url:(.*)访问失败': 'url访问失败',
                                       r'FullGC次数(.*)': 'FullGC次数大于阈值',
                                       r'FullGC平均耗时(.*)': 'FullGC平均耗时大于阈值',
                                       '上I/O等待负载(.*)': 'I/O等待负载过大',
                                       r'(.*)慢响应(.*)': '网页响应慢',
                                       r'硬盘Slot [0, 9]\d{1,2}状态为Failed': '硬盘状态failed',
                                       'Nginx 80端口的连接数大于2000': 'Nginx端口连接数过大',
                                       '上CPU Steal Time持续5分钟超过10%': 'CPU Steal Time持续过高',
                                       r'堆内存平均使用率(.*)': '堆内存平均使用率大于阈值',
                                       'JBOSS 8080端口的连接数大于400': 'JBOSS 8080端口连接数过大',
                                       '网卡eth0(.*)': '网卡接收/发出流量过大',
                                       '(.*)请求延时大于5分钟': '请求延时过大',
                                       '网卡流量unknown': '网卡流量未知',
                                       '空闲交换空间小于50%': '空闲交换空间过小',
                                       r'端口(.*)通信异常': '端口通信异常',
                                       r'空闲CPU为(.*)': '空闲CPU空间持续过小',
                                       r'日志(.*)': '日志包含错误信息',
                                       'sdd IO使用率持续30分钟大于90%': 'sdd IO使用率持续过高',
                                       'sdb IO使用率持续30分钟大于90%': 'sdd IO使用率持续过高',
                                       r'ping丢包率(.*)': 'ping丢包严重',
                                       'ping延迟时间持续3分钟大于100ms': 'ping延迟时间长'}, regex=True, inplace=True)
        self.alarm_type = dict(zip(range(0, len(list(set(df[0])))), list(set(df[0]))))

    def get_alarm_info(self):
        """
        组合告警信息列表
        :return: [timestamp, sys, node, alarm_type]
        """
        for j in path_dct["node_list"][self.flag == 'test']:
            self.train = pd.read_csv(path_dct["new_train"] % j + ".csv", encoding="utf-8")
            with open(f"./data/alarm_infolist/{j}.txt", "a") as f:
                for row in self.train.iterrows():
                    f.write(str([row[1]["time"], row[1]["sysEname"],  row[1]["node_name"],   [k for k, v in self.alarm_type.items() if v == row[1]["trigger"]][0]]))
                    f.write("\n")
            f.close()

    def get_alarm_info_tmp(self, ith):
        """
        :param ith: 第i个告警信息
        :return:
        """
        if self.flag == 'train':
            return pd.read_csv(f'./data/new_train/{ith}.csv', index_col='Unnamed: 0')
        return pd.read_csv(f'./data/new_test/{ith}.csv', index_col='Unnamed: 0')


def preporcess():
    ainfo = AlarmInfo()
    # 更新训练集
    ainfo.add_feature()
    AlarmInfo("test").add_feature()
    # 对告警信息进行分类和存储
    # ainfo.get_alarm_type()  #  暂不需要
    # ainfo.get_alarm_info()  #  暂不需要