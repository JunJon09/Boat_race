#何を買ったかを知らせる。
from email import contentmanager
from LINENotifyBot import LINENotifyBot
import urllib.request
import datetime
import time
from bs4 import BeautifulSoup
from tweet_bot import tweet_bot

def buy_notification(race, stage, memory_race):
    message = str(chenge_number_place(stage))+"競艇場" + ", " + str(race) +"レースの予測\n"
    if memory_race[-1][-1] == '-':
        message += 'エラーが起きたので予測できませんでした。\n\n'
    elif memory_race[-1][-1] == '+':
        message += 'ファイルが存在しなかったので予測しませんでした。\n\n'
    else:
        last_data = memory_race[-1]
        print(last_data)
        count5 = 0
        count6 = 0
        if len(last_data) == 2:
            message += "オッズが低いのでやめました\n"
        #なんかここへん
        #[[2, 6], 'stage', 'race'] 
        elif len(last_data) > 2:
            for last in last_data:
                if not (type(last) is int):
                    if len(last) == 0:
                        continue
                    if last[1] == 5:
                        count5 += 1
                        message += "単勝狙い, 1着: "+ str(last[0]) + "番\n"
                    elif last[1] == 6:
                        count6 += 1
                        message += "複勝狙い, 1着: " + str(last[0]) + "番\n"
            if count5 == 0:
                message += "単勝狙いはオッズが低いからやめました。\n"
            if count6 == 0:
                message += "複勝狙いはオッズが低いからやめました。\n"

        if count5 >= 1 or count6 >= 1:
            try:
                tweet_bot(message)
            except Exception as e:
                print(e, 'ツイッターでエラーが起きてます')
                pass

    LINENotifyBot(message)
    
    # if len(memory_race[-1]) == 5:
    #     message += "購入プログラムでエラーが発生したので購入してません。\n"
    
    # flag = 0
    # if len(memory_race) != 1:
    #     i = -2
    #     while 1:
    #         if len(memory_race) == i * -1:
    #             flag = 1
    #             break
    #         stage = memory_race[i][-1]
    #         if stage != '-':
    #             race = memory_race[i][-2]
    #             break
    #         i -= 1

    #     if flag == 0:
    #         message += "場所:" + str(stage) + ", " + str(race-1) +"レースの結果\n"
    #         today = datetime.date.today()
    #         yyyymmdd = today.strftime('%Y%m%d')
    #         stage = str(stage)
    #         try:
    #             url = "https://www.boatrace.jp/owpc/pc/race/raceresult?rno=" + str(race) + "&jcd=" + str(stage.zfill(2)) + "&hd=" + yyyymmdd
    #             f =  urllib.request.urlopen(url, timeout=3.5)
    #             codeText = f.read().decode("utf-8")
    #             soup = BeautifulSoup(codeText, 'html.parser')
    #             time.sleep(1)

    #             odds =[[0],
    #                             [1],
    #                             [2],
    #                             [3],
    #                             [4],
    #                             [5],
    #                             [6]
    #                             ]
    #             odds_count = 0
    #             #オッズのデータ取得
    #             found = soup.find_all('span', class_='is-payout1')
    #             for i, n in enumerate(found):
    #                 n = n.text.strip()
    #                 if len(n) != 0:
    #                     n = n.replace('¥', '')
    #                     n = n.replace(',', '')
    #                     if i==0 or i==2 or i== 4 or i==6 or i==10 or i==13:
    #                         odds[odds_count].append(int(n))
    #                         odds_count += 1
    #                     elif i==8 or i==9 or i==15 or i==16:
    #                         odds[odds_count].append(int(n))
                
    #             found = soup.find_all('span', class_='numberSet1_number')

    #             message += "1着" + found[0].text.strip() + "番" + "2着" + found[1].text.strip() + "番\n"
    #             # " + "3着" + found[2].text.strip() + "番\n" 
    #             #'オッズ\n3連単:'+ str(odds[0][1]) + " 3連複:"+str(odds[1][1]) + " 2連単:"+str(odds[2][1]) + " 2連複:" +str(odds[3][1]) +
    #             message +=  " 単勝:" + str(odds[5][1])  + " 複勝:" + str(odds[6][1]) + ", " + str(odds[6][2])        

    #         except Exception as e:
    #             print(e)
    #             message += '前の結果でエラーが起きました。'
            
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
    memory_race = [[[2, 6], 1, 11],[[1,6], 1, 11]]
    buy_notification(1, 10, memory_race)