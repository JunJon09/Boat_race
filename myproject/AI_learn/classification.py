#バイナリーファイルのものを持ってきて訓練データとテストデータにわける。

from email import contentmanager
from itertools import count
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
import warnings

def dataSplit(name):
  print('dataSplitがStart!')
  list_std = ['艇番', '全国2連率', '全国勝率', '当地勝率', '当地2連率', 'モータ2連率', 'ボード2連率', '級','展示タイム', 'スタート展示', '天気', 'レーサ番号']
  result_std = ['順位']
  odds_std = ['オッズ']
  try:
    with open(name, 'rb') as web:
      data = pickle.load(web)
  except Exception as e:
    return e
  warnings.simplefilter('ignore', FutureWarning)
  #print(data)
  learn, result, odds, count = split_train_test(data, list_std, result_std)
  number = count/6
  number = int(number * 0.7) * 6
  
  x_train = learn.iloc[0:number]
  x_test = learn.iloc[number:count]
  y_train = result.iloc[0:number]
  y_test = result.iloc[number:count]
  number = count / 6
  number = int(number * 0.7)
  y_odds = odds[number:]
  print(len(y_odds))
  # print(y_odds)
  # print('\n' *100)
  # print(odds)
  return x_train, x_test, y_train, y_test, y_odds

#バイナリーデータから型を変更
def split_train_test(data, list_std, result_std):
  learn = pd.DataFrame(index=[])
  result = pd.DataFrame(index=[])
  count = 0
  odds = []
  er = 0
  er_tmp = []
  for n in data:
    for tmp in n:
      for i, one in enumerate(tmp):
        try:
          
          if i == 6:
            one.append(tmp[7])
            odds.append(one)
          elif i <= 5:
            a = one.pop(-1)
            b = one
            tmp_learn =  pd.Series(b, index=list_std)
            tmp_result = pd.Series(a, index=result_std)
            learn = learn.append(tmp_learn, ignore_index=True)
            result = result.append(tmp_result, ignore_index=True)
            count += 1
        except IndexError as e:
          er_tmp.append(e)
          print(tmp[i], tmp[i-1])
          pass
        except Exception as e:
          #er_tmp.append(e)
          b.insert(9, 1.0)
          tmp_learn =  pd.Series(b, index=list_std)
          tmp_result = pd.Series(a, index=result_std)
          learn = learn.append(tmp_learn, ignore_index=True)
          result = result.append(tmp_result, ignore_index=True)
          count += 1

  print(er_tmp)
  print(count, len(data)*6)

  return learn, result, odds, count