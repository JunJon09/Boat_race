#予測を基に回収率を計算する
from itertools import count
import pickle
from unittest import result

import numpy as np
import matplotlib.pyplot as plt
from urllib3 import Retry


#oddsのファイルの形
#[[[0,三連単], [1, 三連複], [2, 二連単], [3, 二連複], [4, 拡張複], [5, 単勝], [6, 複勝]]]
#とりあえず3連単, 単勝
def recovery_rate(y_test, y_pred, y_odds, x_train):
    print('recovery_rateが実装した')
    predict_rank, result_rank = fix_race_data(y_test, y_pred)
    #hit_result = race_check(predict_rank, result_rank)
    predict_rank, result_rank = soted_rank(predict_rank, result_rank)
    hit_resul = ranck_check(predict_rank, result_rank)
    #回収率の計算
    # Trifecta_recovery_rate = 0
    # Double_single_recovery_rate = 0
    # one_win_recovery_rate = 0
    # count1 = 0
    # count2 = 0
    # count3 = 0
    # Trifecta_plt = []
    # Double_singl_plt = []
    # one_win_recovery_plt= []
    # #[単勝,二連単,3連単]
    # for (hit, odd) in zip(hit_result, y_odds):
    #     Trifecta_recovery_rate -= 100
    #     Double_single_recovery_rate -= 100
    #     one_win_recovery_rate -= 100
    #     for i, o in enumerate(odd):
    #         if i == 5 and hit[0] == 1: #単勝
    #             count1 += 1
    #             one_win_recovery_rate += o[1]
    #             #print('A', o[1], odd[7])
    #         elif i == 2 and hit[1] == 1: #二連単
    #             Double_single_recovery_rate += o[1]
    #             count2 += 1
    #             #print('B', o[1], odd[7])
    #         elif i == 0 and hit[2] == 1: #3連単
    #             Trifecta_recovery_rate += o[1]
    #             count3 += 1
    #             #print('C', o[1], odd[7])
    #     Trifecta_plt.append(Trifecta_recovery_rate)
    #     Double_singl_plt.append(Double_single_recovery_rate)
    #     one_win_recovery_plt.append(one_win_recovery_rate)

    # print(count1, count2, count3, len(hit_result))

    Trifecta_recovery_rate = 0 
    triplet_recovery_rate = 0
    Double_single_recovery_rate = 0
    double_barreled_hatchet_recovery_rate = 0
    one_win_recovery_rate = 0
    placing_bets_recovery_rate = 0
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    count5 = 0
    count6 = 0
    Trifecta_plt = []
    triplet_plt = []
    Double_singl_plt = []
    double_barreled_hatchet_plt = []
    one_win_recovery_plt= []
    placing_bets_plt = []
    #[三連単,三連複,二連単,二連複,拡張,単勝,複勝,]
    for (hit, odd) in zip(hit_resul, y_odds):
        Trifecta_recovery_rate -= 100 
        triplet_recovery_rate -= 100
        Double_single_recovery_rate -= 100
        double_barreled_hatchet_recovery_rate -= 100
        one_win_recovery_rate -= 100
        placing_bets_recovery_rate -= 100
        for i, o in enumerate(odd):
            if i == 0 and hit[0] == 1: #三連単
                Trifecta_recovery_rate += o[1]
                count1 += 1
                # print('A', o[1], odd[7])
            elif i == 1 and hit[1] == 1: #三連複
                triplet_recovery_rate += o[1]
                count2 += 1
                # print('B', o[1], odd[7])
            elif i == 2 and hit[2] == 1: #二連単
                Double_single_recovery_rate += o[1]
                count3 += 1
            elif i == 3 and hit[3] == 1:#二連複
                double_barreled_hatchet_recovery_rate += o[1]
                count4 += 1
            elif i == 4 and hit[4] == 1:#拡張
                print('errrr')
            elif i == 5 and hit[5] == 1:#単勝
                one_win_recovery_rate += o[1]
                count5 += 1
            elif i == 6:
                
                if  hit[6] == 1:#複勝
                    count6 += 1
                    placing_bets_recovery_rate += o[1]
                    print('A', o[1], odd[7])
                if hit[6] == 2:
                    count6 += 1
                    placing_bets_recovery_rate += o[2]
                    print('B', o[2], odd[7],)
                
            
        Trifecta_plt.append(Trifecta_recovery_rate)
        triplet_plt.append(triplet_recovery_rate)
        Double_singl_plt.append(Double_single_recovery_rate)
        double_barreled_hatchet_plt.append(double_barreled_hatchet_recovery_rate)
        one_win_recovery_plt.append(one_win_recovery_rate)
        placing_bets_plt.append(placing_bets_recovery_rate)

    print(count1, count2, count3, count4, count5, count6,len(hit_resul))


    # one_win_recovery_rate = one_win_recovery_rate / ((len(hit_result) * 100)) * 100
    # Double_single_recovery_rate = Double_single_recovery_rate / ((len(hit_result) * 100)) * 100
    # Trifecta_recovery_rate = Trifecta_recovery_rate / ((len(hit_result) * 100)) * 100
    print('*' *100)
    print('結果発表！！')
    print('三連単の回収率 = {}%'.format((Trifecta_recovery_rate/len(hit_resul)/100 + 1)*100))
    print('三連複の回収率 = {}%'.format((triplet_recovery_rate/len(hit_resul)/100 + 1)*100))
    print('二連単の回収率 = {}%'.format((Double_single_recovery_rate/len(hit_resul)/100 + 1) *100))
    print('二連複の回収率 = {}%'.format((double_barreled_hatchet_recovery_rate/len(hit_resul)/100 + 1)*100))
    print('単勝の回収率 = {}%'.format((one_win_recovery_rate/len(hit_resul)/100 + 1) *100))
    print('複勝の回収率 = {}%'.format((placing_bets_recovery_rate/len(hit_resul)/100 + 1)*100))
    print('*' *100)
    print('三連単の当たる確率 = {}%'.format((count1/len(hit_resul)) *100))
    print('三連複の当たる確率 = {}%'.format((count2/len(hit_resul)) *100))
    print('二連単の当たる確率 = {}%'.format((count3/len(hit_resul)) *100))
    print('二連複の当たる確率 = {}%'.format((count4/len(hit_resul)) *100))
    print('単勝の当たる確率 = {}%'.format((count5/len(hit_resul)) *100))
    print('複勝の当たる確率 = {}%'.format((count6/len(hit_resul)) *100))
    print('*' *100)
    print('三連単の利益 = {}円'.format(Trifecta_recovery_rate))
    print('三連複の利益 = {}円'.format(triplet_recovery_rate))
    print('二連単の利益 = {}円'.format(Double_single_recovery_rate))
    print('二連複の利益 = {}円'.format(double_barreled_hatchet_recovery_rate))
    print('単勝の利益 = {}円'.format(one_win_recovery_rate))
    print('複勝の利益 = {}円'.format(placing_bets_recovery_rate))
    print('*' *100)
    print('学習レースデータ: {}件, テストレースデータ: {}件'.format(len(x_train)/6, len(y_test)/6))
    left = np.array([i for i in range(0, len(hit_resul))])
    height = np.array(placing_bets_plt)
    plt.plot(left, height)
    plt.plot(left, height, linewidth=4, color="red")
    plt.title('3win', loc='center')
    plt.show()


    
    
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

    one_reace_results = []
    tmp_result = []
    y_test = y_test.values.tolist()
    for i, result in enumerate(y_test):
        tmp_result.append(result[0])
        if i%6==5:
            one_reace_results.append(tmp_result)
            tmp_result = []
    
    return predict_rank, one_reace_results

#順位の並び替え(test済み)
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
        if predict_rank[0] == real_rank[0]:
            result.append(1)
        else:
            result.append(0)
        
        #複勝
        if predict_rank[0] == real_rank[0]:
            result.append(1)
        elif predict_rank[0] == real_rank[1]:
            result.append(2)
        else:
            result.append(0)
                
        all_result.append(result)
    return all_result
  
def soted_rank(predict_rank, result_rank):
    sorted_predict = []
    sorted_result = []
    for p, r in zip(predict_rank, result_rank):
        predict_3 = []
        result_3 = []
        count = 0
        for (p_3, r_3) in zip(p, r):
            if p_3 == 1:
                predict_3.append(count+1)
            if r_3 == 1:
                result_3.append(count+1)
            count += 1
        count = 0
        for (p_3, r_3) in zip(p, r):
            if p_3 == 2:
                predict_3.append(count+1)
            if r_3 == 2:
                result_3.append(count+1)
            count += 1
        count = 0
        for (p_3, r_3) in zip(p, r):
            if p_3 == 3:
                predict_3.append(count+1)
            if r_3 == 3:
                result_3.append(count+1)
            count += 1
        sorted_predict.append(predict_3)
        sorted_result.append(result_3)
        
    
    return sorted_predict, sorted_result

