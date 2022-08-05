from email import message
import pickle
import lightgbm as lgb
from matplotlib.pyplot import text

def main():
    text = 8
    text = str(text)
    x_train_text = "../../binaryfile/x_train_" + text.zfill(2) + ".binaryfile"
    y_train_text = "../../binaryfile/y_train_" + text.zfill(2) + ".binaryfile"
    x_test_text = "../../binaryfile/x_test_" + text.zfill(2) + ".binaryfile"
    y_test_text = "../../binaryfile/y_test_" + text.zfill(2) + ".binaryfile"
    odds_text = "../../binaryfile/odds_" + text.zfill(2) + ".binaryfile"
    
    with open(x_train_text, 'rb') as web:
        x_train = pickle.load(web)
    web.close
    with open(x_test_text, 'rb') as web:
        x_test = pickle.load(web)
    web.close
    with open(y_train_text, 'rb') as web:
        y_train = pickle.load(web)
    web.close
    with open(y_test_text, 'rb') as web:
        y_test = pickle.load(web)
    web.close
    with open(odds_text, 'rb') as web:
        y_odds = pickle.load(web)
    web.close
    
    #オッズが省略されてるものがあるのでそれを修正してる。
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
                

            
    lgb_train = lgb.Dataset(x_train, y_train)
    lgb_test = lgb.Dataset(x_test, y_test, reference=lgb_train)
    money = 100
    one_memory = []
    sub_memory = []

    for m in range(20):
        rate = 0.01
        one_hight_recovery_rate = 0
        one_hight_money = 0
        one_hight_rate = 0
        one_hight_count = 0
        sub_hight_recovery_rate = 0
        sub_hight_money = 0
        sub_hight_rate = 0
        sub_hight_count = 0
        while(1):
            try:
                params = {'task': 'train',
                            'boosting_type': 'gbdt',
                            # 'objective': 'lambdarank', #←ここでランキング学習と指定！
                            # 'metric': 'ndcg',   # for lambdarank
                            'ndcg_eval_at': [1,2,3,4,5,6],  # 3連単を予測したい
                            'max_position': 6,  # 競艇は6位までしかない
                            'learning_rate': rate, 
                            # 'min_data': 1,
                            # 'min_data_in_bin': 1,
                }
                gbm = lgb.train(params, lgb_train)
                y_pred = gbm.predict(x_test)

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
                        #print(o)
                        #拡張複で同じ同じ数字の時に省略されている
                        #https://www.boatrace.jp/owpc/pc/race/raceresult?rno=8&jcd=23&hd=20220123

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
                            if o[1] <= money:
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
                                if o[1] <=money or o[2] <=money:
                                    placing_bets_recovery_rate += 100
                                    continue
                            else:
                                if o[1] <= money:
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

                if one_win_recovery_rate > one_hight_money:
                    one_hight_recovery_rate = (one_win_recovery_rate/len(hit_resul)/100 + 1) *100
                    one_hight_money = one_win_recovery_rate
                    one_hight_rate = rate
                    one_hight_count = count5
                        
                if   placing_bets_recovery_rate > sub_hight_money:
                    sub_hight_recovery_rate = (placing_bets_recovery_rate/len(hit_resul)/100 + 1) *100
                    sub_hight_money = placing_bets_recovery_rate
                    sub_hight_rate = rate
                    sub_hight_count = count6
                if rate == 1.99:
                    break
                
            except Exception as e: 
                print(e)
                pass
            finally:
                rate += 0.01
                rate = round(rate, 2)
                print(rate)
                print(money)
        one_memory.append(money)
        one_memory.append(one_hight_rate)
        one_memory.append(one_hight_recovery_rate)
        one_memory.append(one_hight_money)
        one_memory.append(one_hight_count)
        
        sub_memory.append(money)
        sub_memory.append(sub_hight_rate)
        sub_memory.append(sub_hight_recovery_rate)
        sub_memory.append(sub_hight_money)
        sub_memory.append(sub_hight_count)
        money += 10

    
    one_hight_money = 0
    sub_hight_money = 0
    file_text = "AI_text/"  + "単勝" + text.zfill(2) + ".txt"
    name = text.zfill(2)
    f = open(file_text, 'w')
    for i, m in enumerate(one_memory):
        text = ""
        text += str(m) + " "
        if i% 5 == 4:
            text += "\n"
        f.write(text)
        if i % 5 == 3:
            if one_hight_money < m:
                one_hight_money = m

    f.write("最大値")
    f.write(str(one_hight_money))
    f.close
    
    file_text = "AI_text/"  + "複勝" + name + ".txt"
    f = open(file_text, 'w')
    for i, m in enumerate(sub_memory):
        text = ""
        text += str(m) + " "
        if i% 5 == 4:
            text += "\n"
        f.write(text)
        if i % 5 == 3:
            if sub_hight_money < m:
                sub_hight_money = m
    
    
    f.write("最大値")
    f.write(str(sub_hight_money))
    f.close
    


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
        # if (predict_rank[0] == real_rank[0] and predict_rank[1] == real_rank[1]) or (predict_rank[0] == real_rank[1] and predict_rank[1] == real_rank[0]):
        #     result.append(1)
        # elif (predict_rank[0] == real_rank[0] and predict_rank[2] == real_rank[2]) or (predict_rank[0] == real_rank[2] and predict_rank[2] == real_rank[0]):
        #     result.append(2)
        # elif (predict_rank[1] == real_rank[1] and predict_rank[2] == real_rank[2]) or (predict_rank[1] == real_rank[2] and predict_rank[2] == real_rank[1]):
        #     result.append(3)
        # else:
        #     result.append(0)
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

if __name__ == '__main__':
    main()