#実際に舟券を購入する
from Get_race_info import Get_race_info
from selenium_buy import selenium_buy
from buy_notification import buy_notification
from predict import predict
import schedule
import time


#グローバル関数としてステージと何レース目かをおいとく
stage = 0
race = 5

#今日何を買ったのか記録
memory_race = []
#レースデータを調べて購入
def Buy_boat():
    print('舟券を買うためのプログラムが実行されました。')
    global race
    race += 1
    stage = 1
    #レースデータを取得する。
    try:
        df = Get_race_info(stage, race)

        #予測をする。
        rank = predict(df)

        #購入
        selenium_buy(rank, stage, race)
    except Exception as e:
        print('エラーが発生しました。よって{}:{}レースは購入を中止しました。'.format(stage, race))
        print(e)
        memory_race.append('-')
    else:
        print('{}:{}レース購入完了しました。'.format(stage, race))
        memory_race.append(rank)
    
    buy_notification(race, stage, memory_race)
       
    


    
    


#稼働する時間をしていする。
def Input_schedule(race_time):
    #今日のレースを確認する。
    print(race_time)

    for data in race_time:
        for i, text in enumerate(data):
            if i>=1:
                for h in text:
                    schedule.every().day.at(h).do(Buy_boat)
            else:
                global stage
                stage = text

    while True:
        schedule.run_pending()
        time.sleep(1)



if __name__ == '__main__':
    Buy_boat()