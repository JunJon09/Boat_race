#今日の買い目の回収率を確認する。
from unittest import TestCase
import urllib.request
import datetime
import time
from bs4 import BeautifulSoup
import traceback

def day_check(memory_race):
    message ="本日購入したレース\n"
    money = 0
    for race in memory_race:
        if race[-1] != '-' and race[-1] != '+' and len(race) > 2:
            today = datetime.date.today()
            yyyymmdd = today.strftime('%Y%m%d')
            stage = str(race[-2])
            R = str(race[-1])
            try:
                url = "https://www.boatrace.jp/owpc/pc/race/raceresult?rno=" + R + "&jcd=" + str(stage.zfill(2)) + "&hd=" + yyyymmdd
                f =  urllib.request.urlopen(url, timeout=3.5)
                codeText = f.read().decode("utf-8")
                soup = BeautifulSoup(codeText, 'html.parser')
                time.sleep(1)
                print(url)

                odds =[[0],
                                [1],
                                [2],
                                [3],
                                [4],
                                [5],
                                [6]
                                ]
                odds_count = 0
                #オッズのデータ取得
                found = soup.find_all('span', class_='is-payout1')
                for i, n in enumerate(found):
                    n = n.text.strip()
                    if len(n) != 0:
                        n = n.replace('¥', '')
                        n = n.replace(',', '')
                        if i==0 or i==2 or i== 4 or i==6 or i==10 or i==13:
                            odds[odds_count].append(int(n))
                            odds_count += 1
                        elif i==8 or i==9 or i==15 or i==16:
                            odds[odds_count].append(int(n))
                
                found = soup.find_all('span', class_='numberSet1_number')
                rank = []
                
                rank.append(int(found[0].text.strip()))
                rank.append(int(found[1].text.strip()))
                rank.append(int(found[2].text.strip()))
                result = []
                count5 = 0
                count6 = 0
                for race_data in race:
                    if not (type(race_data) is int):
                        if len(race_data) == 0:
                            continue
                        if race_data[1] == 5: #買い目単勝
                            count5 += 1
                            result_tmp = []
                            one = race_data[0]
                            result_tmp.append(5)
                            result_tmp.append(one)
                            tmp = 0
                            if one == rank[0]:
                                tmp = 1
                            result_tmp.append(tmp)
                            result.append(result_tmp)
                        elif race_data[1] == 6: #買い目複勝
                            count6 += 1
                            result_tmp = []
                            result_tmp.append(6)
                            sub = race_data[0]
                            result_tmp.append(sub)
                            tmp = ranck_check(sub, rank)
                            result_tmp.append(tmp)
                            result.append(result_tmp)
                #result = [[5, 1], [6, 0]]
                print(len(result))
                money = money - (len(result) * 100) #購入金額
                message = message + str(chenge_number_place(stage)) + "の" + str(R) +"レース結果\n"
                for r in result:
                    if r[0] == 5:
                        message += "単勝予測結果\n"
                        message += "予測1着: " + str(r[1]) + " 結果"
                        if r[2] == 0:
                            message += "ハズレ\n"
                        elif r[2] == 1:
                            message += "当たり: "
                            message += str(odds[5][1]) + "円\n"
                            money += odds[5][1]
                    if r[0] == 6:
                        message += "複勝予測の結果\n"
                        message += "予測1着: " + str(r[1]) + " 結果"
                        if r[2] == 0:
                            message += "ハズレ\n"
                        elif r[2] >= 1:
                            message += "当たり: "
                            message += str(odds[6][r[2]]) + "円\n"
                            money += odds[6][r[2]]
        
                if count5 == 0:
                    message += "単勝狙いはオッズが低いからやめました。\n"
                if count6 == 0:
                    message += "複勝狙いはオッズが低いからやめました。\n"
                # message += "予測:"+ str(race[0]) + "," + str(race[1]) + "," + str(race[2]) + "\n"
                # message += "買い目"
                # for i in buy:
                #     if i == 0:
                #         message += "三連単,"
                #     if i == 1:
                #         message += "三連複,"
                #     if i == 2:
                #         message += "二連単,"
                #     if i == 3:
                #         message += "二連複,"
                #     if i == 4:
                #         message += "拡張,"
                #     if i == 5:
                #         message += "単勝,"
                #     if i == 6:
                #         message += "複勝,"
                #     message = message[:-1]
                #     message += "\n"
                # message += "結果:"+ str(rank[0]) + "," + str(rank[1]) + "," + str(rank[2]) + "\n"
                # for i, f in enumerate(finally_result):
                #     if f == 1:
                #         money = money + odds[i][1]
                #         if i == 0:
                #             message += "三連単当たり:" + str(odds[i][1]) + "円\n"
                #         if i == 1:
                #             message += "三連複当たり:" + str(odds[i][1]) + "円\n"
                #         if i == 2:
                #             message += "二連単当たり:" + str(odds[i][1]) + "円\n"
                #         if i == 3:
                #             message += "二連複当たり:" + str(odds[i][1]) + "円\n"
                #         if i == 4:
                #             message += "拡張当たり:" + str(odds[i][1]) + "円\n"
                #         if i == 5:
                #             message += "単勝当たり:" + str(odds[i][1]) + "円\n"
                #         if i == 6:
                #             message += "複勝当たり:" + str(odds[i][1]) + "円\n"
                #     else:
                #         count += 1
                # if count == 7:
                #     message += '当たりなし\n'


          
            except Exception as e:
                print(e)
                message = 'エラーが起きました。\n'
                print(traceback.format_exc())
                break
    
    message += "今日の収支合計:"+str(money) +"円"
    
    print(message)
    return message, money
    
    
def ranck_check(predict, real):
    #1ならあたり['3連単', '三連複', '二連単', '二連複', '拡張(これは実装しない)', '単勝', '複勝']
    #[2,1,3,[1,2], 'stage', 'race']
    #3連単
    # all_result = []
    # for (predict_rank, real_rank) in zip(predict, real):
    result = 0
        # if predict_rank[0] == real_rank[0] and predict_rank[1] == real_rank[1] and predict_rank[2] == real_rank[2]:
        #     result.append(1)
        # else:
        #     result.append(0)
        
        # #三連複
        # count = 0
        # for i,p in enumerate(predict_rank):
        #     for j, r in enumerate(real_rank):
        #         if i<=2 and j<=2:
        #             if p == r:
        #                 count += 1
        
        # if count == 3:
        #     result.append(1)
        # else:
        #     result.append(0)
        
        # #二連単
        # if (predict_rank[0] == real_rank[0]) and (predict_rank[1] == real_rank[1]):
        #     result.append(1)
        # else:
        #     result.append(0)
        # #二連複
        # count = 0
        # for i,p in enumerate(predict_rank):
        #     for j,r in enumerate(real_rank):
        #         if i<=1 and j<=1:
        #             if p == r:
        #                 count += 1
        # if count == 2:
        #     result.append(1)
        # else:
        #     result.append(0)

        #拡張
        # if (predict_rank[0] == real_rank[0] and predict_rank[1] == real_rank[1]) or (predict_rank[0] == real_rank[1] and predict_rank[1] == real_rank[0]):
        #     result.append(1)
        # elif (predict_rank[0] == real_rank[0] and predict_rank[2] == real_rank[2]) or (predict_rank[0] == real_rank[2] and predict_rank[2] == real_rank[0]):
        #     result.append(2)
        # elif (predict_rank[1] == real_rank[1] and predict_rank[2] == real_rank[2]) or (predict_rank[1] == real_rank[2] and predict_rank[2] == real_rank[1]):
        #     result.append(3)
        # else:
        #     result.append(0)
        # result.append(0)

    # #単勝
    # if predict == real[0]:
    #     result = 1
    # else:
    #     result = 0
    
    #複勝
    if predict == real[0]:
        result = 1
    elif predict == real[1]:
        result = 2
    else:
        result = 0
        
    return result

def chenge_number_place(number):
    text = ""
    number = int(number)
    if number == 1:
        text = "桐生"
    if number == 2:
        text = "戸田"
    if number == 3:
        text = "江戸川"
    if number == 4:
        text = "平和島"
    if number == 5:
        text = "多摩川"
    if number == 6:
        text = "浜名湖"
    if number == 7:
        text = "蒲郡"
    if number == 8:
        text = "常滑"
    if number == 9:
        text = "津"
    if number == 10:
        text = "三国"
    if number == 11:
        text = "びわこ"
    if number == 12:
        text = "住之江"
    if number == 13:
        text = "尼崎"
    if number == 14:
        text = "鳴門"
    if number == 15:
        text = "丸亀"
    if number == 16:
        text = "児島"
    if number == 17:
        text = "宮島"
    if number == 18:
        text = "徳山"
    if number == 19:
        text = "下関"
    if number == 20:
        text = "若松"
    if number == 21:
        text = "芦屋" 
    if number == 22:
        text = "福岡"
    if number == 23:
        text = "唐津"
    if number == 24: 
        text = "大村"

    return text


if __name__ == '__main__':
    #[[1,2,3,[1,2], '-'], [2,1,3,[1,2], 'stage', 'race']]
    memory_race = [[[1, 5],[1, 6], 1, 9], [[3, 5], 1, 10]]
    memory_race = [['+'], [21, 11], ['+'], [18, 11], [[6, 5], 2, 7], ['+'], [[3, 5], 4, 5], ['+'], ['+'], ['+'], ['+'], [[1, 6], 2, 8], [21, 12], [18, 12], ['-'], ['+'], ['+'], ['+'], ['+'], ['+'], [[1, 5], 2, 9], ['+'], [[3, 5], 4, 7], ['+']]
    day_check(memory_race)