from scraping import test
import urllib.request
import pandas as pd


if __name__ == '__main__':
    test()

    
    f =  urllib.request.urlopen('https://kyotei.sakura.ne.jp/kako_kaijyo-09-20211222.html')
    #https://kyotei.sakura.ne.jp/kako_kaijyo-09-20211222.html
    decodeText = f.read().decode("utf-8")
    print(decodeText)
    
     