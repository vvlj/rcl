from sklearn.svm import LinearSVC
from pretreatment.feat_en import FeatureEn
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt
from sklearn.externals import joblib


# 用来正常显示中文标签，SimHei是字体名称，字体必须再系统中存在，字体的查看方式和安装第三部分
plt.rcParams['font.sans-serif']=['SimHei']
# 用来正常显示负号
plt.rcParams['axes.unicode_minus'] = False


def load_data():
    time_feature_lst = []
    fe = FeatureEn()
    for i in range(100):
        time_feature_lst.append(fe.get_time_feature(i, 5, False))
    x, y = [], []
    for i in range(100):
        time_feature, node = time_feature_lst[i]
        print(trans_feature(time_feature))
        x.append(trans_feature(time_feature))
        y.append(0 if node is None else 1)
    return x, y


def trans_feature(time_feature):
    return abs(time_feature.corr()).sum().value_counts(False, sort=False, bins=20).values


def clf_score():
    X_train, X_test, y_train, y_test = train_test_split(*load_data(), test_size=0.2)
    lsvc = LinearSVC(max_iter=100000)
    lsvc.fit(X_train, y_train)
    y_pred = lsvc.predict(X_test)
    return f1_score(y_test, y_pred)


def model_test():
    score_lst = []
    for i in range(100):
        score_lst.append(clf_score())
    plt.plot(range(100), score_lst)
    plt.show()


def dump_model():
    lsvc = LinearSVC(max_iter=100000)
    x, y = load_data()
    lsvc.fit(x, y)
    print("训练F1", f1_score(y, lsvc.predict(x)))
    joblib.dump(lsvc, 'ac_svm.pkl')
    return lsvc


def load_model():
    return joblib.load('ac_svm.pkl')


def get_bar_data(i):
    try:
        lsvc = load_model()
    except Exception as e:
        print(e)
        lsvc = dump_model()

    fe = FeatureEn('test')
    x = trans_feature(fe.get_time_feature(i))
    return x, lsvc.predict([x])[0]


if __name__ == '__main__':
    # 1. 创建./data/new_test
    # 2. 调用get_alarm.preporcess
    dump_model()
    # for i in range(20):
    #     x, y = get_bar_data(i)
    #     plt.bar(range(len(x), y))
    #     plt.show()
