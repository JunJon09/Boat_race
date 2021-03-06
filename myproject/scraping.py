from cmath import exp
from email import contentmanager
import urllib.request
from bs4 import BeautifulSoup
import re
import time
import math
import pickle
import datetime
import timeout_decorator
import traceback
#艇番 名前 全国2連率 全国勝率 当地勝率 当地2連率 モータ2連率 ボード2連率 級 展示タイム スタート展示 天気 着順

def scarpe():
    today = datetime.date.today()
    yyyymmdd = today.strftime('%Y%m%d')
    week = str(yyyymmdd)
    list_std = ['艇番', '全国2連率', '全国勝率', '当地2連率', '当地勝率', 'モータ2連率', 'ボード2連率', '級','展示タイム', 'スタート展示', '天気', 'レーサ番号','順位']
    list_result = ['3連単', '三連複', '二連単', '二連複', '拡張複', '単勝', '複勝']
    #とりあえず津のページの最新を表示
    print('start')
    for stage in range(24):
        all_data = []
        number = str(stage+1)
        number = number.zfill(2)
        count = 0
        for a in range(100):
            try:
                url = 'https://kyotei.sakura.ne.jp/kako_kaijyo-'+ number +'-' + str(20180519) +'.html'
                f =  urllib.request.urlopen(url, timeout=3.5)
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
                    #https://race.kyotei.club/info/20220601-09-1.html"
                    day = re.sub(r"\D", "", link.text)
                    #次のURLに飛ぶ準備
                    more_info_url_tmp.append("https://race.kyotei.club/info/info-" + day + "-" + number +"-")
            except Exception as e:
                print(e)
                print(a)
                print('これは上のエラー')
                continue
            else:
                #12レースあるから
                for link in more_info_url_tmp:
                    twelve_data = []
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
                            f =  urllib.request.urlopen(data, timeout=3.5)
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
                            
                            #着順
                            #最後に代入する
                            arrive = found[3].find_all('div')
                            
                            # 直前予想編   
                            #https://boatrace.jp/owpc/pc/race/beforeinfo?rno=1&jcd=09&hd=20220601  
                            #https://www.boatrace.jp/owpc/pc/race/beforeinfo?rno=7&jcd=20&hd=20220701    
                            target = 'info/'
                            idx = link.find(target)
                            r = link[idx+10:idx+18]
                            data = "https://boatrace.jp/owpc/pc/race/beforeinfo?rno=" + str(x+1) + '&jcd=' + number +'&hd=' + r
                            f =  urllib.request.urlopen(data, timeout=3.5)
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
                            data = "https://boatrace.jp/owpc/pc/race/raceresult?rno=" + str(x+1) + '&jcd='+ number + '&hd=' + r
                            f =  urllib.request.urlopen(data, timeout=3.5)
                            codeText = f.read().decode("utf-8")
                            soup = BeautifulSoup(codeText, 'html.parser')
                            time.sleep(1)

                            found = soup.find_all('span', class_='is-fs12')
                            for i, n in enumerate(found):
                                n = n.text.strip()
                                df[i].append(int(n))

                        
                            #前取ってあった着順を代入
                            #1位〜3位の順位で同着だった場合データを取ら無い。
                            rank = []
                            for n in arrive:
                                n = n.text.strip()
                                rank.append(n)

                            if rank.count("1") >= 2 or rank.count("2") >= 2 or rank.count("3") >= 2:
                                raise ValueError("同着なのでリストの中には入れません")

                            for i, n in enumerate(rank):
                                df[i].append(int(n))
                            
                            
                                

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

                            #オッズとどこの何レース日にちを入れてる。
                            #01-2-2021-09-01 1場所の2Rの2021年9月1日
                            df.append(odds)
                            race_day = data.replace('https://boatrace.jp/owpc/pc/race/raceresult?rno=', 'race=')
                            race_day = race_day.replace('&jcd=', 'stage=')
                            race_day = race_day.replace('&hd=', 'day=')
                            df.append(race_day)
                        except Exception as e:
                            print(e)
                            print(data)
                            print(traceback.format_exc())
                        else:
                            print(df)
                            twelve_data.append(df)
                            
                            count += 1
                        finally:
                            df = []
                            odds = []
                    
                    all_data.insert(0, twelve_data)
                    print(all_data)
                    print('*'*100)
            print('-'*200)           
        print('最終日:{}'.format(week))
        print('場所:{}'.format(stage))
        print('レースデータ件数:'.format(count))
        file_name = 'boat' + number + '.binaryfile'
        with open(file_name, 'wb') as web:
            pickle.dump(all_data, web)
        web.close
    print("終了")
    
        
#偏差値
def  deviation_value(scores, df):
    hensachi = []
    average = sum(scores) / len(scores)
    zure_sum = 0
    for score in scores:
        zure = round((score - average)**2, 1)
        zure_sum += zure
    variance = zure_sum/len(scores)#分散
    standard_deviation = math.sqrt(variance) #標準偏差
    if standard_deviation == 0:
        for i in range(6):
            df[i].append(50)
    else:
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


if __name__ == '__main__':
    scarpe()
