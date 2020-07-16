from pretreatment.feat_en import get_time_freq_feature
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import calinski_harabaz_score
from sklearn import preprocessing

# 取10分钟，单位时间
# 时间频率聚类

time_length = 10 * 60
delta = 5
time_freq_feature = {}
for i in range(100):
    if i == 17:
        continue
    time_freq_feature[i] = get_time_freq_feature(i, delta)[:int(time_length / delta)]
df = pd.DataFrame(time_freq_feature)
min_max_scaler = preprocessing.MinMaxScaler()
X = min_max_scaler.fit_transform(df)

inertia_score = []
for k in range(2, 10):
    model = KMeans(k)
    model.fit(X)
    print(model.inertia_)
    inertia_score.append(model.inertia_)  # 越小越好
