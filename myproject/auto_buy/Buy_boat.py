#実際に舟券を購入する
from fileinput import filename
from turtle import left
from Get_race_info import Get_race_info
from selenium_buy import selenium_buy
from buy_notification import buy_notification
from predict import predict
from day_check import day_check
from LINENotifyBot import LINENotifyBot
import schedule
import time
import pickle
import numpy as np
import matplotlib.pyplot as plt

#グローバル関数としてステージと何レース目かをおいとく


#今日何を買ったのか記録
memory_race = []
#memory_race = [[1,2,3,[0], 1, 1], [4,3,5,[6], 1, 12]]
stage_race = []
#レースデータを調べて購入
def Buy_boat(stage):
    print('舟券を買うためのプログラムが実行されました。')
    stage_race[stage] += 1
    race = stage_race[stage]
    global memory_race
    #レースデータを取得する。
    try:
        df = Get_race_info(stage, race)

        #予測をする。
        rank = predict(df, stage)

        #購入
        selenium_buy(rank, stage, race)
        
    except ValueError as e:
        print('エラーが発生しました。よって{}:{}レースは購入を中止しました。'.format(stage, race))
        rank.append('-')
        memory_race.append(rank)
    except Exception as e:
        print('エラーが発生しました。よって{}:{}レースは購入を中止しました。'.format(stage, race))
        print(e)
        memory_race.append('-')
    else:
        print('{}:{}レース購入完了しました。'.format(stage, race))
        rank.append(stage)
        rank.appned(race)
        memory_race.append(rank)
        #[[1,2,3,[1,2], '-'], [2,1,3,[1,2], 'stage', 'race']]
    
    buy_notification(race, stage, memory_race)

#1日の収支をラインに知らせる。
def day_notification():
    print(memory_race)
    message, money = day_check(memory_race)
    try:
        with open('../../binaryfile/money.binaryfile', 'rb') as web:
            all_money = pickle.load(web)
        web.close
        last_money = all_money[-1]
        real_money = last_money - money
        all_money.append(real_money)
        figure, ax = plt.subplots() #グラフの定義
        x = [i+1 for i in range(len(all_money))]
        y = all_money
        ax.plot(x,y) 
        figure.savefig('../../PLT/test.jpg')
        with open('../../binaryfile/money.binaryfile', 'wb') as web:
            pickle.dump(all_money, web)
        web.close
        filename = '../../PLT/test.jpg'

    except Exception as e:
        print(e)
        pass
    
    LINENotifyBot(message, filename)
    
    

#稼働する時間をしていする。
def Input_schedule(race_time):
    #今日のレースを確認する。
    # global memory_race
    global stage_race
    memory_race = []
    stage_race = [0 for i in range(25)]
    for data in race_time:
        print(data)
        for text in data[1]:
            schedule.every().day.at(text).do(Buy_boat, stage=data[0])
    schedule.every().days.at("23:00").do(day_notification)
    while True:
        schedule.run_pending()
        time.sleep(1)



if __name__ == '__main__':
    Buy_boat()