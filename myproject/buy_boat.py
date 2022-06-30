#実際に舟券を購入する
import urllib.request

def buy_boat():
    #今日のレースを確認する。
    day = '20220702'
    stage = '01'
    url = 'https://boatrace.jp/owpc/pc/race/racelist?rno=1&jcd='+stage+'&hd=' + day
    #https://boatrace.jp/owpc/pc/race/racelist?rno=1&jcd=01&hd=20220305
    f =  urllib.request.urlopen(url, timeout=3.5)
    20:37, 15:21