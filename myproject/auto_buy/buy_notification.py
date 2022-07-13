#何を買ったかを知らせる。
from LINENotifyBot import LINENotifyBot
import urllib.request
import datetime
import time
from bs4 import BeautifulSoup
def buy_notification(race, stage, memory_race):
    message = "場所:" + str(stage) + ", " + str(race) +"レースの予測\n"
    if memory_race[-1][0] == '-':
        message += 'エラーが起きたので予測できませんでした。\n\n'
    else:
        message += "1着" +  str(memory_race[-1][0]) + "番 " + "2着" + str(memory_race[-1][1]) + "番 " + "3着" + str(memory_race[-1][2])+ "番\n"

    if len(memory_race[-1]) == 5:
        message += "購入プログラムでエラーが発生したので購入してません。\n"

    if len(memory_race) != 1:
        message += "場所:" + str(stage) + ", " + str(race-1) +"レースの結果\n"
        today = datetime.date.today()
        yyyymmdd = today.strftime('%Y%m%d')
        stage = str(stage)
        try:
            url = "https://www.boatrace.jp/owpc/pc/race/raceresult?rno=" + str(race-1) + "&jcd=" + str(stage.zfill(2)) + "&hd=" + yyyymmdd
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
                    if int(n) < 100:
                        raise ValueError("100円より低いものを確認しました。")
                    if i==0 or i==2 or i== 4 or i==6 or i==10 or i==13:
                        odds[odds_count].append(int(n))
                        odds_count += 1
                    elif i==8 or i==9 or i==15 or i==16:
                        odds[odds_count].append(int(n))
            
            found = soup.find_all('span', class_='numberSet1_number')

            message += "1着" + found[0].text.strip() + "番 " + "2着" + found[1].text.strip() + "番 " + "3着" + found[2].text.strip() + "番\n"
            message += 'オッズ\n3連単:'+ str(odds[0][1]) + " 3連複:"+str(odds[1][1]) + " 2連単:"+str(odds[2][1]) + " 2連複:" +str(odds[3][1]) + " 単勝:" + str(odds[5][1])         

        except Exception as e:
            print(e)
            message += '前の結果でエラーが起きました。'
        

    LINENotifyBot(message)
       
        


