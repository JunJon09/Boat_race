#実際に舟券を購入する
from Get_race_info import Get_race_info
from predict import predict
import schedule
import time

#グローバル関数としてステージと何レース目かをおいとく
stage = 0
race = 0
#レースデータを調べて購入
def Buy_boat():
    print('舟券を買うためのプログラムが実行されました。')
    global race
    race += 1
    stage = 1
    #レースデータを取得する。
    df = Get_race_info(stage, race)

    #予測をする。
    result = predict(df)

    #購入
    

    
    


#稼働する時間をしていする。
def Input_schedule(race_time):
    #今日のレースを確認する。
    print(race_time)

    for data in race_time:
        for i, text in enumerate(data):
            
            print(text)
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