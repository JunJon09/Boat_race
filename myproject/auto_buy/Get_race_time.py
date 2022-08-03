#今日がどこのレースで何時からか行うかとってくる。
#[[1, [1015, 1030, 1045, 1130]], [2, [1015, 1030, 1045, 1130]]] 1の会場で10:15, 10:30, 10:45, 11:30みたいに返す。
from email import contentmanager
import urllib.request
from bs4 import BeautifulSoup
import datetime
import time
def Get_race_time(): 
    today_race_time = []
    today = datetime.date.today()
    yyyymmdd = today.strftime('%Y%m%d')
    #yyyymmdd = '20220804'

    try:
        url = "https://www.boatrace.jp/owpc/pc/race/index?hd=" + yyyymmdd
        f =  urllib.request.urlopen(url, timeout=3.5)
        codeText = f.read().decode("utf-8")
        soup = BeautifulSoup(codeText, 'html.parser')
        time.sleep(1)
        found = soup.find_all('ul', class_='textLinks3')

    except Exception as e:
        print(url)
        print(e)
        exit()
    
    now_race = []
    for i in found:
        try:
            url = "https://www.boatrace.jp/"
            url += i.find('a').get('href')
            now_race.append(url)
        except AttributeError:
            continue

    for url in now_race:
        race = []
        try:
            f =  urllib.request.urlopen(url, timeout=3.5)
            codeText = f.read().decode("utf-8")
            soup = BeautifulSoup(codeText, 'html.parser')
            time.sleep(1)

            found = soup.find_all('div', class_='h-mt10')
            # found = found.find('tr')
            # print(found)
            stage = found[0].find('thead').find('a').get('href')
            stage = stage.replace('/owpc/pc/race/racelist?rno=1&jcd=', '')
            cat = '&hd=' + yyyymmdd
            stage = stage.replace(cat, '')
            if stage[0] == '0':
                stage = stage[1]
            stage = int(stage)
            race.append(stage)
            
            f = found[0]
            f = f.find('tbody').text.replace('\n', ',')
            f = f.replace(' ', '')
            f = f.replace("締切予定時刻", '')
            race_time=f.split(',')
            del race_time[0:3]
            del race_time[-2:]
            five_ago_race_time = []
            for r in race_time:
                dte = five_ago(r)
                five_ago_race_time.append(dte)
            race.append(five_ago_race_time)
        except Exception as e:
            print(e)
            #continue
        else:
            today_race_time.append(race)
    
    #ここで本当は自動入力、時間がないから手動
    #15:17	15:45	16:10	16:35	17:07	17:35	18:03	18:32	19:02	19:33	20:05	20:37
    #5分前に動かす。
    #race = [1, ['15:14', '15:44', '16:00', '16:30', '16:54', '17:22', '17:50', '18:22', '18:52', '19:18', '19:49', '20:36']]
    today_race_time = []
    today_race_time.append([10, ['15:18', '15:42', '16:06', '16:33', '16:57', '17:28', '17:59', '18:31', '19:03', '19:35', '20:02', '22:02']])
    return today_race_time
    
def five_ago(text):
    day = text.split(':')
    M = day[1]
    M = int(M)
    M -= 5
    H = day[0]
    if M < 0:
        H = int(H)
        H -= 1
        H = str(H)
        #6を06に
        H = H.zfill(2)
        M = 60 + M
        str(M)
    else:
        M = str(M)
        M = M.zfill(2)
    
    day = str(H) + ":" + str(M)

    return day
    
if __name__ == '__main__':
    Get_race_time()
    