#ランダムフォレストを使って学習

from pprint import pformat
from pyexpat.errors import XML_ERROR_TAG_MISMATCH
from tkinter.tix import Y_REGION
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LinearRegression
import pandas as pd
import lightgbm as lgb
import numpy as np
import matplotlib.pyplot as plt
import lightgbm as lgb
import time



from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
def algorithm(x_train, x_test, y_train, y_test):
    #分類
    # clf = RandomForestClassifier(max_depth=30, n_estimators=30, random_state=42)
    # clf.fit(x_train, y_train.values.ravel())
    # y_pred = clf.predict(x_test)
    #回帰
      # reg_lr = LinearRegression()
      # reg_lr.fit(x_train, y_train.values.ravel())
      # y_pred_1 = reg_lr.predict(x_test)
    # #標準化偏回帰係数を求めてる
    # coef_df = pd.DataFrame(reg_lr.coef_,x_train.columns)
    # # print(coef_df)
      
    
      lgb_train = lgb.Dataset(x_train, y_train)
      lgb_test = lgb.Dataset(x_test, y_test, reference=lgb_train)
      params = {'task': 'train',
                  'boosting_type': 'gbdt',
                  # 'objective': 'lambdarank', #←ここでランキング学習と指定！
                  # 'metric': 'ndcg',   # for lambdarank
                  'ndcg_eval_at': [1,2,3,4,5,6],  # 3連単を予測したい
                  'max_position': 6,  # 競艇は6位までしかない
                  'learning_rate': 1.61, 
                  # 'min_data': 1,
                  # 'min_data_in_bin': 1,
      }
      lgb_results = {} 
      gbm = lgb.train(params, lgb_train)
      test_predicted = gbm.predict(x_test)
      print(test_predicted)
      # y_pred = model.predict(x_test)
    # print(y_pred_1)
   #
    
    
      return y_test, test_predicted