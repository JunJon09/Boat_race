#バイナリーファイルのものを持ってきて訓練データとテストデータにわける。

from itertools import count
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split


def dataSplit(name):
  print('dataSplitがStart!')
  list_std = ['艇番', '全国2連率', '全国勝率', '当地勝率', '当地2連率', 'モータ2連率', 'ボード2連率', '級','展示タイム', 'スタート展示', '天気', 'レーサ番号']
  result_std = ['順位']
  try:
    with open(name, 'rb') as web:
      data = pickle.load(web)
  except Exception as e:
    return e
    
  learn, result, count= split_train_test(data, list_std, result_std)

  number = count/6
  number = int(number * 0.7) * 6

  x_train = learn.iloc[0:number]
  x_test = learn.iloc[number:count]
  y_train = result.iloc[0:number]
  y_test = result.iloc[number:count]
  return x_train, x_test, y_train, y_test

#バイナリーデータから型を変更
def split_train_test(data, list_std, result_std):
  learn = pd.DataFrame(index=[])
  result = pd.DataFrame(index=[])
  count = 0
  for n in data:
    for i in n:
      a = i.pop(-1)
      b = i
      tmp_learn =  pd.Series(b, index=list_std)
      tmp_result = pd.Series(a, index=result_std)
      learn = learn.append(tmp_learn, ignore_index=True)
      result = result.append(tmp_result, ignore_index=True)
      count += 1
  
  return learn, result, count
  
  
  