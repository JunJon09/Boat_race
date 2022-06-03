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
    
    more_info_url = []
    #12レースあるから
    for link in more_info_url_tmp:
        for i in range(12):
            more_info_url.append(link + str(i+1) + '.html')
            
    #↑ここまででそのページの情報のURLを取得できた。
    
    for link in more_info_url:
        #ここで順位表を取れるとこまでできた。
        f =  urllib.request.urlopen(link)
        codeText = f.read().decode("utf-8")
        print(codeText)
        time.sleep(1)
    #何のデータを取得するか
    #何号艇,身長、体重、順位、全国の２連率、当地の2連率、モータ、ボート、級、年齢、名前
    #公式サイトから取ってくる物
    #展示タイム、スタート展示、気温、天気、風速、波
    
