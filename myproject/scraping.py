import urllib.request
import pandas as pd
import sys, pprint
from bs4 import BeautifulSoup
import re
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
        day = re.sub(r"\D", "", link.text)
        #次のURLに飛ぶ準備
        
        more_info_url_tmp.append("https://race.kyotei.club/info/" + day + "-09-")
    
    more_info_url = []
    #12レースあるから
    for link in more_info_url_tmp:
        for i in range(12):
            more_info_url.append(link + str(i+1) + '.html')
            
    #↑ここまででそのページの情報のURLを取得できた。
    
    
            
        
        
        
