#データをもとに予測する。
import pandas as pd
import pickle
import lightgbm as lgb

def predict(df, stage):
    list_std = ['艇番', '全国2連率', '全国勝率', '当地勝率', '当地2連率', 'モータ2連率', 'ボード2連率', '級','展示タイム', 'スタート展示', '天気', 'レーサ番号']
    result_std = ['順位']
    odds_std = ['オッズ']
    stage = str(stage)
    one_params_rate = {'01': 1.71, '02': 1.83, '03': 1.47, '04': 1.93, '05': 1.80, '06': 1.66, '07': 1.86, '08': 0, '09': 0, '10': 0, '11': 0, '12': 0, '13': 0, '14': 0, '15': 0, '16': 0, '17': 0, '18': -1, '19': 1.76, '20': 0, '21': 1.59, '22': 1.92, '23':1.9, '24': -1}
    sub_params_rate = {'01': 1.95, '02': 1.92, '03': 1.88, '04': 1.84, '05': 1.75, '06': 1.84, '07': 1.86, '08': 0, '09': 0, '10': 0, '11': 0, '12': 0, '13': 0, '14': 0, '15': 0, '16': 0, '17': 0, '18': 1.93, '19': 1.79, '20': 0, '21': 1.75, '22': 1.94, '23':1.9, '24': 1.61}
    #前はデータをバイナリファイルに入れてなかったからここでデータをセットしてるが今ではそのデータがあるのでそれを読み込む
    #後は会場ごとにLightGBMの値が違うからそれを変更すること。オッズも(ここにリストを作っといてぶち込めばいけると思う)
    data = []
    x_text = '../../binaryfile/x_train_' + stage.zfill(2) +'.binaryfile'
    y_train = '../../binaryfile/y_train_' + stage.zfill(2) +'.binaryfile'

    with open(x_text, 'rb') as web:
        x_train = pickle.load(web)
    web.close

    with open(y_train, 'rb') as web:
        y_train = pickle.load(web)
    web.close

    #ここでファイルがない時のエラーが発生ここを修正

    
    
    one_rate = one_params_rate[stage.zfill(2)]
    sub_rate = sub_params_rate[stage.zfill(2)]
    lgb_train = lgb.Dataset(x_train, y_train)
    #データセット
    #もしデータがない場合returndataが空白になる。
    if one_rate > 0:
        params = {'task': 'train',
                                    'boosting_type': 'gbdt',
                                    # 'objective': 'lambdarank', #←ここでランキング学習と指定！
                                    # 'metric': 'ndcg',   # for lambdarank
                                    'ndcg_eval_at': [1,2,3,4,5,6],  # 3連単を予測したい
                                    'max_position': 6,  # 競艇は6位までしかない
                                    'learning_rate': one_rate, 
                                    # 'min_data': 1,
                                    # 'min_data_in_bin': 1,
        }
        #学習
        gbm = lgb.train(params, lgb_train)
        
        #決定
        y_pred = gbm.predict(df)

        rank = [0, 0, 0, 0, 0, 0]
        #[2.1, 1.9, 1.3, 4.1, 3.0, 5.0]
        for i, n in enumerate(sorted(y_pred)): #低い順番に並べ直す　
            for j, m in enumerate(y_pred):
                if n == m:
                    rank[j] = i + 1 

        #[3, 2, 1, 5, 4, 6]
        
        r_3 = []
        for i, number in enumerate(rank):
            if number == 1:
                r_3.append(i+1)

        r_3.append(5)

        data.append(r_3)

    #複勝
    if sub_rate > 0:
        params = {'task': 'train',
                                    'boosting_type': 'gbdt',
                                    # 'objective': 'lambdarank', #←ここでランキング学習と指定！
                                    # 'metric': 'ndcg',   # for lambdarank
                                    'ndcg_eval_at': [1,2,3,4,5,6],  # 3連単を予測したい
                                    'max_position': 6,  # 競艇は6位までしかない
                                    'learning_rate': sub_rate, 
                                    # 'min_data': 1,
                                    # 'min_data_in_bin': 1,
        }
        #学習
        gbm = lgb.train(params, lgb_train)
        
        #決定
        y_pred = gbm.predict(df)

        rank = [0, 0, 0, 0, 0, 0]
        #[2.1, 1.9, 1.3, 4.1, 3.0, 5.0]
        for i, n in enumerate(sorted(y_pred)): #低い順番に並べ直す　
            for j, m in enumerate(y_pred):
                if n == m:
                    rank[j] = i + 1 

        
        r_3 = []
        for i, number in enumerate(rank):
            if number == 1:
                r_3.append(i+1)

        r_3.append(6)

        data.append(r_3)

    #data=[1,5,3,6]
    #配列1番目と3番目の5と6は単勝とかの話
    
    return data



