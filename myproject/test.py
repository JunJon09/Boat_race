from email import message
from unittest import result
import requests
import pickle
import schedule
import time
import matplotlib.pyplot as plt



def sample():
    predict = []
    result = []
    #1
    tmp_predict = [1.1, 2.3, 4.2, 4.1, 3.1, 2.0]
    tmp_result = [1, 3, 6, 5, 4, 2]
    predict.append(tmp_predict)
    result.append(tmp_result)
    #2
    tmp_predict = [1.5, 2.2, 5.2, 1.1, 3.1, 1.0]
    tmp_result = [3, 4, 6, 2, 5, 1]
    predict.append(tmp_predict)
    result.append(tmp_result)
    #3
    tmp_predict = [1.5, 2.3, 1.2, 3.1, 3.3, 2.5]
    tmp_result = [2, 3, 1, 5, 6, 4]
    predict.append(tmp_predict)
    result.append(tmp_result)
    #4
    tmp_predict = [1.4, 1.3, 3.2, 2.1, 3.6, 2.5]
    tmp_result = [2, 1, 5, 3, 6, 4]
    predict.append(tmp_predict)
    result.append(tmp_result)
    #5
    tmp_predict = [2.1, 4.3, 4.2, 4.0, 1.1, 2.0]
    tmp_result = [3, 6, 5, 4, 1, 2]
    predict.append(tmp_predict)
    result.append(tmp_result)
    #6
    tmp_predict = [1.9, 1.91, 2.2, 1.901, 1.9111, 2.0]
    tmp_result = [1, 3, 6, 2, 4, 5]
    predict.append(tmp_predict)
    result.append(tmp_result)
    #7
    tmp_predict = [1.3, 1.2, 5.1, 1.4, 1.1, 1.0]
    tmp_result = [4, 3, 6, 5, 2, 1]
    predict.append(tmp_predict)
    result.append(tmp_result)
    #8
    tmp_predict = [2.1, 2.3, 1.2, 3.1, 3.3, 2.5]
    tmp_result = [2, 3, 1, 5, 6, 4]
    predict.append(tmp_predict)
    result.append(tmp_result)
    #9
    tmp_predict = [1.401, 1.4, 3.1, 2.1111, 3.33, 1.5]
    tmp_result = [2, 1, 5, 4, 6, 3]
    predict.append(tmp_predict)
    result.append(tmp_result)
    #10
    tmp_predict = [3.1, 4.3, 1.2, 2.00000, 1.9, 1.9001]
    tmp_result = [5, 6, 1, 4, 2, 3]
    predict.append(tmp_predict)
    result.append(tmp_result)

    return predict , result

#順位の並び替え
def rank_sort(up_sort, normal_sort):
    rank = [0, 0, 0, 0, 0, 0]
    for i, n in enumerate(up_sort):
        for j, m in enumerate(normal_sort):
            if n == m:
                rank[j] = i + 1
    
    return rank
#予測が当たってるか
def race_check(predict_rank, result_rank):
    hit_result = []
    Trifecta_flag = 0 #三連単
    Triple_flag = 0 #三連複
    Double_single_flag = 0 #二連単
    Double_double_flag = 0 #二連複
    one_win_flag = 0 #単勝
    Double_win = 0 #複勝
    ream_count = 0 #連単カウント
    hit_tmp = []
    for (predict, result) in zip(predict_rank, result_rank):
        for i, (p, r) in enumerate(zip(predict, result)):
            if i<= 2 and p == r:
                ream_count += 1
            
        if ream_count == 0: #[単勝,二連単,3連単]
            hit_tmp = [0, 0, 0]
        elif ream_count == 1:
            hit_tmp = [1, 0, 0]
        elif ream_count == 2:
            hit_tmp = [1, 1, 0]
        elif ream_count == 3:
            hit_tmp = [1, 1, 1]

        hit_result.append(hit_tmp)
        hit_tmp = []
        ream_count = 0

    return hit_result         


def ranck_check(predict, real):
    #1ならあたり['3連単', '三連複', '二連単', '二連複', '拡張(これは実装しない)', '単勝', '複勝']
    #[2,1,3,[1,2], 'stage', 'race']
    #3連単
    all_result = []
    for (predict_rank, real_rank) in zip(predict, real):

        result = []
        if predict_rank[0] == real_rank[0] and predict_rank[1] == real_rank[1] and predict_rank[2] == real_rank[2]:
            result.append(1)
        else:
            result.append(0)
        
        #三連複
        count = 0
        for i,p in enumerate(predict_rank):
            for j, r in enumerate(real_rank):
                if i<=2 and j<=2:
                    if p == r:
                        count += 1
        
        if count == 3:
            result.append(1)
        else:
            result.append(0)
        
        #二連単
        if (predict_rank[0] == real_rank[0]) and (predict_rank[1] == real_rank[1]):
            result.append(1)
        else:
            result.append(0)
        #二連複
        count = 0
        for i,p in enumerate(predict_rank):
            for j,r in enumerate(real_rank):
                if i<=1 and j<=1:
                    if p == r:
                        count += 1
        if count == 2:
            result.append(1)
        else:
            result.append(0)

        #拡張
        result.append(0)

        #単勝
        if predict_rank[0] == real_rank [0]:
            result.append(1)
        else:
            result.append(0)
        
        #複勝
        count = 0
        for i, r in enumerate(real_rank):
            if i<=1:
                if r == predict_rank[0]:
                    count += 1
        
        if count == 1:
            result.append(1)
        else:
            result.append(1)
        all_result.append(result)
    return all_result
    

if __name__ == '__main__':
    predict, result = sample()
    tmp = []
    for i in predict:
        tmp.append(rank_sort(sorted(i), i))
    
    for (a, b) in zip(tmp, result):
        for (c, d) in zip(a, b):
            if c!= d:
                print('error!')
                print(a, b)
        
    

    

    