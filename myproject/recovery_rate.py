#予測を基に回収率を計算する
import pickle

#oddsのファイルの形
#[[[0,三連単], [1, 三連複], [2, 二連単], [3, 二連複], [4, 拡張複], [5, 単勝], [6, 複勝]]]
#とりあえず3連単, 単勝
def recovery_rate(y_test, y_pred, Odds_file):
    print('recovery_rateが実装した')
    try:
        with open(Odds_file, 'rb') as web:
            Odds = pickle.load(web)
    except Exception as e:
        return e
    
    
    predict_rank, one_reace_result = fix_race_data(y_test, y_pred)
    print(len(predict_rank))
    print(len(one_reace_result))
    odds = Odds[-1*len(predict_rank):]

    
    
    
    
    
#1レース6人にちゃんとした
def fix_race_data(y_test, y_pred):
    one_race_data = []
    tmp_data = []
    for i, data in enumerate(y_pred):
        tmp_data.append(data)
        if(i % 6 == 5):
            one_race_data.append(tmp_data)
            tmp_data = []

    predict_rank = []
    for one_race in one_race_data:
        tmp = rank_sort(sorted(one_race), one_race)
        predict_rank.append(tmp)

    one_reace_result = []
    tmp_result = []
    y_test = y_test.values.tolist()
    for i, result in enumerate(y_test):
        tmp_result.append(result[0])
        if i%6==5:
            one_reace_result.append(tmp_result)
            tmp_result = []
    
    return predict_rank, one_reace_result

#順位の並び替え
def rank_sort(up_sort, normal_sort):
    rank = [0, 0, 0, 0, 0, 0]
    for i, n in enumerate(up_sort):
        for j, m in enumerate(normal_sort):
            if n == m:
                rank[j] = i + 1
    
    return rank


    
    

