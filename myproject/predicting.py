import pandas as pd
import pickle
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

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
  
  pd.set_option('display.max_rows', None)
  print(learn)
  train_X, test_X, train_Y, test_Y = train_test_split(learn, result,                # 訓練データとテストデータに分割する
                                                    test_size=0.3,       # テストデータの割合
                                                    shuffle=True,        # シャッフルする
                                                    random_state=0)      # 乱数シードを固定する
  lgb_train = lgb.Dataset(train_X, train_Y)
  lgb_test = lgb.Dataset(test_X, test_Y, reference=lgb_train)
  
  lgbm_params =  {
    'task': 'train',
    'boosting_type': 'gbdt',
    'objective': 'lambdarank', #←ここでランキング学習と指定！
    'metric': 'ndcg',   # for lambdarank
    'ndcg_eval_at': [1,2,3],  # 3連単を予測したい
    'max_position': 6,  # 競艇は6位までしかない
    'learning_rate': 0.01, 
    'min_data': 1,
    'min_data_in_bin': 1,
#     'num_leaves': 31,
#     'min_data_in_leaf': 20,
#     'max_depth':35,
  }
  
  lgtrain = lgb.Dataset(train_X, train_Y)
  lgvalid = lgb.Dataset(test_X, test_Y)
  lgb_clf = lgb.train(
      lgbm_params,
      lgtrain,
      num_boost_round=250,
      valid_sets=[lgtrain, lgvalid],
      valid_names=['train','valid'],
      early_stopping_rounds=20,
      verbose_eval=5
  )
  y_pred = lgb_clf.predict(val_onehot,group=val_group, num_iteration=lgb_clf.best_iteration)