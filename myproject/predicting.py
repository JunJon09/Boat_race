import pandas as pd
import pickle
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn import metrics
import numpy as np


def predict():
  with open('boat-tsu.binaryfile', 'rb') as web:
    boat_tsu = pickle.load(web)
  
  list_std = ['艇番', '全国2連率', '全国勝率', '当地勝率', '当地2連率', 'モータ2連率', 'ボード2連率', '級', '展示タイム', 'スタート展示', '天気']
  
  result_std = ['順位']
  le = preprocessing.LabelEncoder()
  #行
  learn = pd.DataFrame(index=[])
  result = pd.DataFrame(index=[])
  for n in boat_tsu:
    for i in n:
      # labels_id = le.fit_transform(i)
      # i[1] = labels_id[1]
      i.pop(1)
      a = i.pop(-1)
      b = i
      tmp_learn =  pd.Series(b, index=list_std)
      tmp_result = pd.Series(a, index=result_std)
      learn = learn.append(tmp_learn, ignore_index=True)
      result = result.append(tmp_result, ignore_index=True)
  
  
  train_x, test_x, train_y, test_y = train_test_split(learn, result, random_state=1)
  lgb_train = lgb.Dataset(train_x, train_y)
  lgb_eval = lgb.Dataset(test_x, test_y, reference=lgb_train)
  parms = {
    'task': 'train', #トレーニング用
    'boosting': 'gbdt', #勾配ブースティング決定木
    'objective': 'multiclass', #目的：多値分類
    'num_class': 11 , #分類するクラス数
    'metric': 'multi_error', #評価指標：正答率
    'num_iterations': 1000, #1000回学習
    'verbose': -1 #学習情報を非表示
  }   
  
  model = lgb.train(parms,
                 #訓練データ
                 train_set=lgb_train,
                 # 評価データ
                 valid_sets=lgb_eval,
                 early_stopping_rounds=100)
  
  y_pred = model.predict(test_x)
# 予測確率を整数へ
  y_pred = np.argmax(y_pred, axis=1) 

  print(metrics.classification_report(test_y, y_pred))