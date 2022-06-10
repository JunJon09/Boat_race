import urllib.request
from bs4 import BeautifulSoup
import re
import time
import math
import pickle

#何のデータを取得するか
#何号艇,(身長、体重)、順位、全国の２連率、当地の2連率、モータ、ボート、級、(年齢)、名前
#公式サイトから取ってくる物
#展示タイム、スタート展示、気温、天気、(風速、波)
#艇番 名前 全国2連率 全国勝率 当地勝率 当地2連率 モータ2連率 ボード2連率 級 展示タイム スタート展示 天気 着順

def scarpe():
    week = '20220601'
    list_std = ['艇番', '全国2連率', '全国勝率', '当地勝率', '当地2連率', 'モータ2連率', 'ボード2連率', '級','展示タイム', 'スタート展示', '天気', 'レーサ番号','順位']
    all_data = []
    #とりあえず津のページの最新を表示
    print('start')
    for i in range(100):
        url = 'https://kyotei.sakura.ne.jp/kako_kaijyo-09-' + week +'.html'
        f =  urllib.request.urlopen(url)
        time.sleep(1)
        #fをいつも書くhtmlに変換
        codeText = f.read().decode("utf-8")
        soup = BeautifulSoup(codeText, 'html.parser')
        more_info_url_tmp = []
        #日付を取る
        for i, link in enumerate(soup.find_all('strong')):
            if(i == len(soup.find_all('strong'))-1):
                week = re.sub(r"\D", "", link.text)
                continue
            #"https://race.kyotei.club/info/info-20220601-09-1.html"
            #:https://race.kyotei.club/info/20220601-09-1.html"
            day = re.sub(r"\D", "", link.text)
            #次のURLに飛ぶ準備
            more_info_url_tmp.append("https://race.kyotei.club/info/info-" + day + "-09-")
            
        #12レースあるから
        for link in more_info_url_tmp:
            for x in range(12):
                try:
                    df =[  [1],
                    [2],
                    [3],
                    [4],
                    [5],
                    [6]
                    ]
                    data = link + str(x+1) + '.html'
                    
                    
                    #ここで順位表を取れるとこまでできた。
                    f =  urllib.request.urlopen(data)
                    codeText = f.read().decode("utf-8")
                    soup = BeautifulSoup(codeText, 'html.parser')
                    found = soup.find('div', class_='race_list_box_table')
                    found = found.find_all('tr')
                    
                    time.sleep(1)
                            
                    #全国の2連率と全国の勝率
                    natonal_two = found[21].find_all('div')
                    df = two_world(natonal_two, df)
                    
                    #当地の2連率と勝率
                    locational_two = found[22].find_all('div') 
                    df = two_world(locational_two, df)
                            
                    #モータの2連率
                    motor_two = found[23].find_all('span')
                    df = boat_motor(motor_two, df)
                        
                    #ボートの2連率
                    boat_two = found[24].find_all('span')
                    df = boat_motor(boat_two, df)
                    
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
                    time.sleep(1)
                        
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
                        
                    #https://boatrace.jp/owpc/pc/race/raceresult?rno=1&jcd=09&hd=20220427
                    #レーサ番号
                    data = "https://boatrace.jp/owpc/pc/race/raceresult?rno=" + str(x+1) + '&jcd=09&hd=' + r
                    f =  urllib.request.urlopen(data)
                    codeText = f.read().decode("utf-8")
                    soup = BeautifulSoup(codeText, 'html.parser')
                    time.sleep(1)
                    found = soup.find_all('span', class_='is-fs12')
                    for i, n in enumerate(found):
                        n = n.text.strip()
                        df[i].append(int(n))
                
                    #前取ってあった着順を代入
                    for i, n in enumerate(arrive):
                        n = n.text.strip()
                        df[i].append(int(n))
                
                except Exception as e:
                    print(e)
                    print(link)
                else:
                    all_data.append(df)
                finally:
                    df = []
        print('-'*100)           
    print("終了")
    print(week)
    with open('boat-tsu_handred.binaryfile', 'wb') as web:
        pickle.dump(all_data, web) 
        
#偏差値
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
    
#選手の2連率    
def two_world(html, df):
    deviation = []
    tmp = []
    for i, n in enumerate(html):
        if(i%3 == 0):
            deviation.append(float(n.text))
        if(i%3 == 2):
            tmp.append(float(n.text))
    df = deviation_value(deviation, df)
    df = deviation_value(tmp, df)
    return df
#モータとボートの2連率
def boat_motor(html, df):
    deviation = []
    for i, n in enumerate(html):
        deviation.append(float(n.text))
    df = deviation_value(deviation, df)
    return df
