#何を買ったかを知らせる。
from email import contentmanager
from LINENotifyBot import LINENotifyBot
import urllib.request
import datetime
import time
from bs4 import BeautifulSoup
def buy_notification(race, stage, memory_race):
    message = "場所:" + str(stage) + ", " + str(race) +"レースの予測\n"
    if memory_race[-1][-1] == '-':
        message += 'エラーが起きたので予測できませんでした。\n\n'
    elif memory_race[-1][-1] == '+':
        message += 'ファイルが存在しなかったので予測しませんでした。\n\n'
    else:
        last_data = memory_race[-1]
        print(len(last_data))
        count5 = 0
        count6 = 0
        if len(last_data) == 2:
            message += "オッズが低いのでやめました\n"

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


    if len(memory_race[-1]) == 5:
        message += "購入プログラムでエラーが発生したので購入してません。\n"
    
    flag = 0
    if len(memory_race) != 1:
        i = -2
        while 1:
            if len(memory_race) == i * -1:
                flag = 1
                break
            stage = memory_race[i][-1]
            if stage != '-':
                race = memory_race[i][-2]
                break
            i -= 1
        if flag == 0:
            message += "場所:" + str(stage) + ", " + str(race-1) +"レースの結果\n"
            today = datetime.date.today()
            yyyymmdd = today.strftime('%Y%m%d')
            stage = str(stage)
            try:
                url = "https://www.boatrace.jp/owpc/pc/race/raceresult?rno=" + str(race) + "&jcd=" + str(stage.zfill(2)) + "&hd=" + yyyymmdd
                f =  urllib.request.urlopen(url, timeout=3.5)
                codeText = f.read().decode("utf-8")
                soup = BeautifulSoup(codeText, 'html.parser')
                time.sleep(1)

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

                message += "1着" + found[0].text.strip() + "番" + "2着" + found[1].text.strip() + "番\n"
                # " + "3着" + found[2].text.strip() + "番\n" 
                #'オッズ\n3連単:'+ str(odds[0][1]) + " 3連複:"+str(odds[1][1]) + " 2連単:"+str(odds[2][1]) + " 2連複:" +str(odds[3][1]) +
                message +=  " 単勝:" + str(odds[5][1])  + " 複勝:" + str(odds[6][1]) + ", " + str(odds[6][2])        

            except Exception as e:
                print(e)
                message += '前の結果でエラーが起きました。'
            

    LINENotifyBot(message)
    
if __name__ == '__main__':
    memory_race = [[[2, 6], 1, 12],[[], 1, 12]]
    buy_notification(1, 12, memory_race)