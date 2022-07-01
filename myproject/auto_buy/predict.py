#データをもとに予測する。

import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LinearRegression

def predict(df):
    list_std = ['艇番', '全国2連率', '全国勝率', '当地勝率', '当地2連率', 'モータ2連率', 'ボード2連率', '級','展示タイム', 'スタート展示', '天気', 'レーサ番号']
    result_std = ['順位']
    odds_std = ['オッズ']
    try:
        with open('../../binaryfile/boat01.binaryfile', 'rb') as web:
            data = pickle.load(web)
    except Exception as e:
        return e

    #データセット
    learn, result, odds, count = split_train_test(data, list_std, result_std)
    x_train = learn
    y_train = result
    df = real_split(df, list_std)
    #学習
    reg_lr = LinearRegression()
    reg_lr.fit(x_train, y_train.values.ravel())

    #決定
    y_pred = reg_lr.predict(df)

    print(y_pred)
    rank = [0, 0, 0, 0, 0, 0]
    for i, n in enumerate(sorted(y_pred)):
        for j, m in enumerate(y_pred):
            if n == m:
                rank[j] = i + 1

    print(rank)

    
    return rank




#バイナリーデータから型を変更
def split_train_test(data, list_std, result_std):
  
    learn = pd.DataFrame(index=[])
    result = pd.DataFrame(index=[])
    count = 0
    odds = []
    er = 0
    er_tmp = []
    for n in data:
        for i, one in enumerate(n):
            try:
                if i == 6:
                    one.append(n[7])
                    odds.append(one)
                elif i <= 5:
                    a = one.pop(-1)
                    b = one
                    tmp_learn =  pd.Series(b, index=list_std)
                    tmp_result = pd.Series(a, index=result_std)
                    learn = learn.append(tmp_learn, ignore_index=True)
                    result = result.append(tmp_result, ignore_index=True)
                    count += 1
                
            except Exception as e:
                er_tmp.append(e)
                b.insert(9, 1.0)
                tmp_learn =  pd.Series(b, index=list_std)
                tmp_result = pd.Series(a, index=result_std)
                learn = learn.append(tmp_learn, ignore_index=True)
                result = result.append(tmp_result, ignore_index=True)
                count += 1

    print(er_tmp)
    print(count, len(data)*6)

    return learn, result, odds, count

def real_split(df, list_std):
    learn = pd.DataFrame(index=[])
    for n in df:
        tmp_learn =  pd.Series(n, index=list_std)
        learn = learn.append(tmp_learn, ignore_index=True)
    return learn

