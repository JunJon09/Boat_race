#レースの選手情報を取得する。

import datetime
import urllib.request
from bs4 import BeautifulSoup
import time
import math

#['艇番', '全国2連率', '全国勝率', '当地2連率', '当地勝率', 'モータ2連率', 'ボード2連率', '級','展示タイム', 'スタート展示', '天気', 'レーサ番号']
def Get_race_info(stage, race):
    #https://www.boatrace.jp/owpc/pc/race/beforeinfo?rno=1&jcd=01&hd=20220623
    #https://www.boatrace.jp/owpc/pc/race/racelist?rno=1&jcd=01&hd=20220601
    try:
        stage = str(stage)
        today = datetime.date.today()
        yyyymmdd = today.strftime('%Y%m%d')
        url = 'https://www.boatrace.jp/owpc/pc/race/racelist?rno='+ str(race) +'&jcd='+ str(stage.zfill(2)) +'&hd=' + yyyymmdd
        #url = 'https://www.boatrace.jp/owpc/pc/race/racelist?rno=5&jcd=01&hd=20220703'
        
        #1Day
        #3R!1
        #6R1,2
        #7R1,2
        #9R1
        #10R1
        #11R1

        #1470円
        #560円

        #2Day
        #6 1, 140
        #7 1, 2:150, 270
        #11 1, 140
        #12 1, 170

        #600
        # 270



        f =  urllib.request.urlopen(url, timeout=3.5)
        time.sleep(1)
        codeText = f.read().decode("utf-8")
        soup = BeautifulSoup(codeText, 'html.parser')
        
        #'全国2連率', '全国勝率', '当地2連率', '当地勝率', 'モータ2連率', 'ボード2連率',
        found = soup.find_all('td', class_='is-lineH2')

        df =[[1],
            [2],
            [3],
            [4],
            [5],
            [6]
        ]
        
        #でーたの加工
        tmp = []
        for i, text in enumerate(found):
            if i % 5 != 0:
                for j, n in enumerate(text):
                    n = n.text.strip()
                    if len(n) != 0:
                        tmp.append(float(n))
        whole_win = []
        whole_two_win = []
        local_win = []
        local_two_win = []
        mota_two_win = []
        boat_two_win = []

        for i, text in enumerate(tmp):
            if i % 12 == 0:
                whole_win.append(text)
            elif i % 12 == 1:
                whole_two_win.append(text)
            elif i % 12 == 3:
                local_win.append(text)
            elif i % 12 == 4:
                local_two_win.append(text)
            elif i % 12 == 7:
                mota_two_win.append(text)
            elif i % 12 == 10:
                boat_two_win.append(text)
        
        deviation_value(whole_two_win, df)
        deviation_value(whole_win, df)
        deviation_value(local_two_win, df)
        deviation_value(local_win, df)
        deviation_value(mota_two_win, df)
        deviation_value(boat_two_win, df)

        #級とレーサ番号
        player_class = []
        player_number = []
        found = soup.find_all('div', class_='is-fs11')
        for i, data in enumerate(found):
            if i % 2 == 0:
                data = data.text.replace(' ', '')
                data = data.replace('\n', '')
                data = data.split('/')
                player_number.append(int(data[0]))
                player_class.append(data[1])

        for i, number in enumerate(player_class):
            n = 0
            if number == 'A1':
                n = 1
            elif number == 'A2':
                n = 2
            elif number == 'A3':
                n = 3
            elif number == 'B1':
                n = 4
            else:
                n = 5
            df[i].append(n)

        
        #https://www.boatrace.jp/owpc/pc/race/beforeinfo?rno=7&jcd=20&hd=20220701
        #https://www.boatrace.jp/owpc/pc/race/beforeinfo?rno=3&jcd=01&hd=20220704
        #https:/www./boatrace.jp/owpc/pc/race/beforeinfo?rno=3&jcd=01&hd=20220704
        url = "https://www.boatrace.jp/owpc/pc/race/beforeinfo?rno=" + str(race) + '&jcd=' + str(stage.zfill(2)) +'&hd=' + yyyymmdd
        #url ='https://www.boatrace.jp/owpc/pc/race/beforeinfo?rno=7&jcd=20&hd=20220701'
        f =  urllib.request.urlopen(url, timeout=3.5)
        codeText = f.read().decode("utf-8")
        soup = BeautifulSoup(codeText, 'html.parser')
        time.sleep(1)
        found= soup.find_all('tbody', class_='is-fs12')

        #展示タイム
        for i, data in enumerate(found):
            data = data.text.replace(' ', '')
            data = data.replace('\n', '!')
            data = data.replace('\u3000', '')
            data = data.split('!')
            df[i].append(data[6])
    
        #スタート展示
        found = soup.find_all('span', class_='table1_boatImage1Time')
        for i, n in enumerate(found):
            n = n.text
            if 'F' in n:
                n = n.replace('F', '-')
            n = n.replace('.', '0.')
            #1.1の時10.1になる.普通.11→0.11
            if float(n) >= 10.0 or float(n) <= -10.0:
                n = n.replace('0.', '.')
            df[i].append(float(n))

        #天気'晴れ'=1,'曇り'=2, '雨'=3, '風'=4, '雪'=5
        found = soup.find_all('div', class_='weather1_bodyUnitLabel')
        wether = found[1].text.strip()
        if wether == '晴れ':
            wether = 0
        elif wether == '曇り':
            wether = 1
        elif wether == '雨':
            wether = 2
        elif wether == '風':
            wether = 3
        elif wether == '雪':
            wether = 4
        else:
            wether = 5
        for i in range(6):
            df[i].append(wether)
        

        for i, number in  enumerate(player_number):
            df[i].append(number)

        print(df, url)

    except Exception as e:
        print(e)
        

    return df


def  deviation_value(scores, df):
    hensachi = []
    average = sum(scores) / len(scores)
    zure_sum = 0
    for score in scores:
        zure = round((score - average)**2, 1)
        zure_sum += zure
    variance = zure_sum/len(scores)
    standard_deviation = math.sqrt(variance)
    for score in scores:
        hensachi.append(round(((score-average)/standard_deviation)*10 + 50, 1))
    for i, n in enumerate(hensachi):
        df[i].append(n)
    return df