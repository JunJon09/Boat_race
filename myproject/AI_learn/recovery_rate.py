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
    odds_tmp = y_odds
    for i, odd in enumerate(odds_tmp):
        for j, o in enumerate(odd):
            if j == 5 and len(o) >= 3:
                tmp = y_odds[i][j-1].pop(-1)
                a = y_odds[i][j].pop(1)
                b = y_odds[i][j].pop(1)
                y_odds[i][j].append(tmp)
                y_odds[i][j+1].append(a)
                y_odds[i][j+1].append(b)
    predict_rank, result_rank = fix_race_data(y_test, y_pred)
    predict_rank, result_rank = soted_rank(predict_rank, result_rank)
    hit_resul = ranck_check(predict_rank, result_rank)

    Trifecta_recovery_rate = 0 
    triplet_recovery_rate = 0
    Double_single_recovery_rate = 0
    double_barreled_hatchet_recovery_rate = 0
    one_win_recovery_rate = 0
    placing_bets_recovery_rate = 0
    Extended_duplication_rate = 0
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    count5 = 0
    count6 = 0
    count7 = 0
    hit_list = [[0,0,0,0,0,0] for i in range(7)]
    Trifecta_plt = []
    triplet_plt = []
    Double_singl_plt = []
    double_barreled_hatchet_plt = []
    one_win_recovery_plt= []
    placing_bets_plt = []
    Extended_duplication_plt = []
    #[三連単,三連複,二連単,二連複,拡張,単勝,複勝,]
    for (hit, odd) in zip(hit_resul, y_odds):
        Trifecta_recovery_rate -= 100 
        triplet_recovery_rate -= 100
        Double_single_recovery_rate -= 100
        double_barreled_hatchet_recovery_rate -= 100
        one_win_recovery_rate -= 100
        placing_bets_recovery_rate -= 100
        Extended_duplication_rate -= 100
        
        for i, o in enumerate(odd):
            if i == 0 and hit[0] == 1: #三連単
                Trifecta_recovery_rate += o[1]
                count1 += 1
                if o[1] < 1000:
                    hit_list[0][0] += 1
                elif o[1] < 2500:
                    hit_list[0][1] += 1
                elif o[1] < 5000:
                    hit_list[0][2] += 1
                elif o[1] < 10000:
                    hit_list[0][3] += 1
                else:
                    hit_list[0][4] += 1

                # print('A', o[1], odd[7])
            elif i == 1 and hit[1] == 1: #三連複
                triplet_recovery_rate += o[1]
                count2 += 1
                if o[1] < 1000:
                    hit_list[1][0] += 1
                elif o[1] < 2000:
                    hit_list[1][1] += 1
                elif o[1] < 3000:
                    hit_list[1][2] += 1
                elif o[1] < 4000:
                    hit_list[1][3] += 1
                else:
                    hit_list[1][4] += 1
                # print('B', o[1], odd[7])
            elif i == 2 and hit[2] == 1: #二連単
                Double_single_recovery_rate += o[1]
                count3 += 1
                if o[1] < 300:
                    hit_list[2][0] += 1
                elif o[1] < 600:
                    hit_list[2][1] += 1
                elif o[1] < 1000:
                    hit_list[2][2] += 1
                elif o[1] < 1500:
                    hit_list[2][3] += 1
                else:
                    hit_list[2][4] += 1
            elif i == 3 and hit[3] == 1:#二連複
                double_barreled_hatchet_recovery_rate += o[1]
                count4 += 1
                if o[1] < 200:
                    hit_list[3][0] += 1
                elif o[1] < 400:
                    hit_list[3][1] += 1
                elif o[1] < 600:
                    hit_list[3][2] += 1
                elif o[1] < 1000:
                    hit_list[3][3] += 1
                else:
                    hit_list[3][4] += 1
            elif i == 4:
                if hit[4] == 1:
                    Extended_duplication_rate += o[1]
                    count7 += 1
                elif hit[4] == 2:
                    Extended_duplication_rate += o[2]
                    count7 += 1
                elif hit[4] == 3:
                    Extended_duplication_rate += o[3]
                    count7 += 1
            elif i == 5:#単勝     
                if o[1] <= 280:
                    one_win_recovery_rate += 100
                else:
                    if hit[5] == 1:       
                        one_win_recovery_rate += o[1]
                        count5 += 1
                        if o[1] < 200:
                            hit_list[4][0] += 1
                        elif o[1] < 400:
                            hit_list[4][1] += 1
                        elif o[1] < 600:
                            hit_list[4][2] += 1
                        elif o[1] < 1000:
                            hit_list[4][3] += 1
                        else:
                            hit_list[4][4] += 1
                        if (o[1] < 120):
                            hit_list[4][5] += 1
                    
            elif i == 6:
                if len(o) >=3:
                    if o[1] <=210 or o[2] <= 210:
                        placing_bets_recovery_rate += 100
                        continue
                else:
                    if o[1] <= 210:
                        placing_bets_recovery_rate += 100
                        continue
                
                    
                if  hit[6] == 1:#複勝
                    count6 += 1
                    placing_bets_recovery_rate += o[1]
                    if o[1] < 200:
                        hit_list[5][0] += 1
                    elif o[1] < 400:
                        hit_list[5][1] += 1
                    elif o[1] < 600:
                        hit_list[5][2] += 1
                    elif o[1] < 1000:
                        hit_list[5][3] += 1
                    else:
                        hit_list[5][4] += 1
                    if (o[1] <=110):
                        hit_list[5][5] += 1
                    
                if hit[6] == 2:
                    if len(o) == 2:
                        placing_bets_recovery_rate += 100
                        continue
                    count6 += 1
                    placing_bets_recovery_rate += o[2]
                    if o[1] < 200:
                        hit_list[5][0] += 1
                    elif o[1] < 400:
                        hit_list[5][1] += 1
                    elif o[1] < 600:
                        hit_list[5][2] += 1
                    elif o[1] < 1000:
                        hit_list[5][3] += 1
                    else:
                        hit_list[5][4] += 1
                    if (o[2] < 120):
                        hit_list[5][5] += 1
                
            
        Trifecta_plt.append(Trifecta_recovery_rate)
        triplet_plt.append(triplet_recovery_rate)
        Double_singl_plt.append(Double_single_recovery_rate)
        double_barreled_hatchet_plt.append(double_barreled_hatchet_recovery_rate)
        one_win_recovery_plt.append(one_win_recovery_rate)
        placing_bets_plt.append(placing_bets_recovery_rate)
        Extended_duplication_plt.append(Extended_duplication_rate)

    print(count1, count2, count3, count4, count5, count6,count7, len(hit_resul))


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
    print('拡幅の回収率 = {}%'.format((Extended_duplication_rate/len(hit_resul)/100 + 1)*100))
    print('*' *100)
    print('三連単の当たる確率 = {}%'.format((count1/len(hit_resul)) *100))
    print('三連複の当たる確率 = {}%'.format((count2/len(hit_resul)) *100))
    print('二連単の当たる確率 = {}%'.format((count3/len(hit_resul)) *100))
    print('二連複の当たる確率 = {}%'.format((count4/len(hit_resul)) *100))
    print('単勝の当たる確率 = {}%'.format((count5/len(hit_resul)) *100))
    print('複勝の当たる確率 = {}%'.format((count6/len(hit_resul)) *100))
    print('拡幅の当たる確率 = {}%'.format((count7/len(hit_resul)) *100))
    print('*' *100)
    print('三連単の利益 = {}円'.format(Trifecta_recovery_rate))
    print('三連複の利益 = {}円'.format(triplet_recovery_rate))
    print('二連単の利益 = {}円'.format(Double_single_recovery_rate))
    print('二連複の利益 = {}円'.format(double_barreled_hatchet_recovery_rate))
    print('単勝の利益 = {}円'.format(one_win_recovery_rate))
    print('複勝の利益 = {}円'.format(placing_bets_recovery_rate))
    print('拡幅の利益 = {}円'.format(Extended_duplication_rate))
    print('*' *100)
    print('学習レースデータ: {}件, テストレースデータ: {}件'.format(len(x_train)/6, len(y_test)/6))
    print(hit_list)
    left = np.array([i for i in range(0, len(hit_resul))])
    height = np.array(placing_bets_plt)
    plt.plot(left, height)
    plt.plot(left, height, linewidth=4, color="red")
    plt.title('3win', loc='center')
    #plt.show()


    
    
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
        #ここでもし毎回買い目を1,2,3にする。
        tmp = rank_sort(sorted(one_race), one_race)
        #tmp = [1, 2, 3, 4, 5, 6]
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
        if (predict_rank[0] == real_rank[0] and predict_rank[1] == real_rank[1]) or (predict_rank[0] == real_rank[1] and predict_rank[1] == real_rank[0]):
            result.append(1)
        elif (predict_rank[0] == real_rank[0] and predict_rank[2] == real_rank[2]) or (predict_rank[0] == real_rank[2] and predict_rank[2] == real_rank[0]):
            result.append(2)
        elif (predict_rank[1] == real_rank[1] and predict_rank[2] == real_rank[2]) or (predict_rank[1] == real_rank[2] and predict_rank[2] == real_rank[1]):
            result.append(3)
        else:
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

