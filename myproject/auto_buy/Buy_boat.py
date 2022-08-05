#実際に舟券を購入する
from fileinput import filename
from turtle import left
from Get_race_info import Get_race_info
from myproject.Auto_buy.tweet_bot import tweet_bot
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
import datetime
import traceback
from tweet_bot import tweet_bot
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
    buy = []
    global memory_race
    #レースデータを取得する。
    try:
        df = Get_race_info(stage, race)

        #予測をする。
        rank = predict(df, stage)
        print(rank, '---')
        if len(rank) == 0:
            raise ValueError()
        #rankが空白の時がある。まだデータを取ってきてないもの

        #購入
        buy = selenium_buy(rank, stage, race)
        print(buy, 'aaaa')

    except ValueError as e:
        print('エラーが発生しました。よって{}:{}レースは購入を中止しました。'.format(stage, race))
        buy.append('-')
        memory_race.append(buy)
        print(traceback.format_exc())
    except  FileNotFoundError:
        buy.append('+')
        print('ファイルが存在しませんでした')
        memory_race.append(buy)
    except Exception as e:
        print('エラーが発生しましたよって{}:{}レースは購入を中止しました。'.format(stage, race))
        print(e)
        memory_race.append('-')
        print(traceback.format_exc())
    else:
        if len(buy) == 0:
            print('{}:{}オッズが低いので購入しませんでした'.format(stage, race))
        else:
            print('{}:{}レース購入完了しました。'.format(stage, race))
        buy.append(stage)
        buy.append(race)
        print(buy)
        memory_race.append(buy)
        #[[1,5], [2,6], '-'], [[2, 6], 'stage', 'race']
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
        real_money = last_money + money
        all_money.append(real_money)
        message += "\n総合収支:" + str(real_money) + "円です\n"
        figure, ax = plt.subplots() #グラフの定義
        plt.xlabel('Day') #X軸ラベル
        plt.ylabel('Profit') #Y軸ラベル 
        plt.title("Recovery_rate")
        x = [i+1 for i in range(len(all_money))]
        y = all_money
        ax.plot(x,y)
        today = datetime.date.today()
        yyyymmdd = today.strftime('%Y%m%d')
        day_text = '../../PLT/' + yyyymmdd + ".jpg"
        figure.savefig(day_text)
        with open('../../binaryfile/money.binaryfile', 'wb') as web:
            pickle.dump(all_money, web)
        web.close

        #収支合計をテキストに代入
        file_text = "../../Result/"  + "毎日収支.txt"
        text_data = yyyymmdd + "日の収支: " + str(money) + "円, " + "合計収支: " + str(real_money) + "円\n"
        with open(file_text, mode='a') as f:
            f.write(text_data)
        f.close
    except Exception as e:
        print(e)
        pass
    
    LINENotifyBot(message, day_text)
    try:
        tweet_bot(message)
    except Exception as e:
        print(e, 'ツイッターでエラーが起きてます')
        pass
    exit(0)
    
    

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
    schedule.every().days.at("17:26").do(day_notification)
    while True:
        schedule.run_pending()
        time.sleep(1)



if __name__ == '__main__':
    a = [[[1,5], [2,6], 3, 10], [[], 5, 10]]
    buy_notification(10, 2, a)