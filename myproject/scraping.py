import urllib.request
import pandas as pd
import sys, pprint
from bs4 import BeautifulSoup
import re
import time
def scarpe():
    #とりあえず津のページの最新を表示
    f =  urllib.request.urlopen('https://kyotei.sakura.ne.jp/kako_stdm-tsu.html')
    #fをいつも書くhtmlに変換
    codeText = f.read().decode("utf-8")
    
    soup = BeautifulSoup(codeText, 'html.parser')
    more_info_url_tmp = []
    #日付を取る
    for link in soup.find_all('strong'):
        #"https://race.kyotei.club/info/info-20220601-09-1.html"
        #:https://race.kyotei.club/info/20220601-09-1.html"
        day = re.sub(r"\D", "", link.text)
        #次のURLに飛ぶ準備
        
        more_info_url_tmp.append("https://race.kyotei.club/info/info-" + day + "-09-")
    
    list_std = ['艇番', '名前', '全国2連率', '全国勝率', '当地勝率', '当地2連率', 'モータ2連率', 'ボード2連率', '級', '展示タイム', 'スタート展示', '天気', '順位']
    
    df =[  [1],
            [2],
            [3],
            [4],
            [5],
            [6]
        ]
    #12レースあるから
    for link in more_info_url_tmp:
        for x in range(12):
            data = link + str(x+1) + '.html'
            
            
            #ここで順位表を取れるとこまでできた。
            f =  urllib.request.urlopen(data)
            codeText = f.read().decode("utf-8")
            soup = BeautifulSoup(codeText, 'html.parser')
            found = soup.find('div', class_='race_list_box_table')
            found = found.find_all('tr')
            
            #氏名
            names = found[1].find_all('span')
            for i,name in enumerate(names):
                if(i % 4 == 0):
                    df[int(i/4)].append(name.text.replace('\u3000', ''))
                    
            #全国の2連率と全国の勝率
            natonal_two = found[21].find_all('div') 
            for i, n in enumerate(natonal_two):
                if(i%3==0):
                    df[int(i/3)].append(float(n.text))
                if(i%3==2):
                    df[int(i/3)].append(float(n.text))
            
            #当地の2連率と勝率
            locational_two = found[22].find_all('div') 
            for i, n in enumerate(locational_two):
                if(i%3==0):
                    df[int(i/3)].append(float(n.text))
                if(i%3==2):
                    df[int(i/3)].append(float(n.text))
                    
            #モータの2連率
            motor_two = found[23].find_all('span')
            for i, n in enumerate(motor_two):
                df[i].append(float(n.text))
                
            #ボートの2連率
            boat_two = found[24].find_all('span')
            for i, n in enumerate(boat_two):
                df[i].append(float(n.text))
            
            #級 A1=1 A2=2 A3=3 B1=4 B2=5
            count = 0
            for i in range(9, 20, 2):
                n = found[i].text.replace('\n', '')
                if(n == 'A1'):
                    n = 1
                elif(n == 'A2'):
                    n = 2
                elif(n == 'A3'):
                    n = 3
                elif(n == 'B1'):
                    n = 4
                else:
                    n = 5
                df[count].append(n)
                count += 1
                
            #展示タイム
            before_time = found[6].find_all('div')
            for i, n in enumerate(before_time):
                n = n.text.strip()
                df[i].append(float(n))
            time.sleep(1)
            
            #着順
            #最後に代入する
            arrive = found[3].find_all('div')
           
            
            # 直前予想編   
            #https://boatrace.jp/owpc/pc/race/beforeinfo?rno=1&jcd=09&hd=20220601      
                    
            
            target = 'info/'
            idx = link.find(target)
            r = link[idx+10:idx+18]
            data = "https://boatrace.jp/owpc/pc/race/beforeinfo?rno=" + str(x+1) + '&jcd=09&hd=' + r
            f =  urllib.request.urlopen(data)
            codeText = f.read().decode("utf-8")
            soup = BeautifulSoup(codeText, 'html.parser')
            
            found = soup.find_all('span', class_='table1_boatImage1Time')
            
            #スタート展示
            for i, n in enumerate(found):
                n = n.text
                if 'F' in n:
                    n = n.replace('F', '-')
                n = n.replace('.', '0.')
                #1.1の時10.1になる.普通.11→0.11
                if float(n) >= 10.0 or float(n) <= -10.0:
                    n = n.replace('0.', '.')
                df[i].append(float(n))
                
            #天気
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
           
            

            #前取ってあった着順を代入
            for i, n in enumerate(arrive):
                n = n.text.strip()
                df[i].append(int(n))
           
            print(df)
            time.sleep(1)
            
            
            
    
    #↑ここまででそのページの情報のURLを取得できた。
    
    #何のデータを取得するか
    #何号艇,(身長、体重)、順位、全国の２連率、当地の2連率、モータ、ボート、級、(年齢)、名前
    #公式サイトから取ってくる物
    #展示タイム、スタート展示、気温、天気、(風速、波)
    
    #艇番 名前 全国2連率 全国勝率 当地勝率 当地2連率 モータ2連率 ボード2連率 級 展示タイム スタート展示 天気 着順
    
   
    
    
