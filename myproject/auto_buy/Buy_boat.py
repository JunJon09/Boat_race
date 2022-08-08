#実際に舟券を購入する
from fileinput import filename
from turtle import left
from Get_race_info import Get_race_info
from selenium_buy import selenium_buy
from buy_notification import buy_notification
from predict import predict
from day_check import day_check
from LINENotifyBot import LINENotifyBot
from tweet_bot import tweet_bot
import schedule
import time
import pickle
import numpy as np
import matplotlib.pyplot as plt
import datetime
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By

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
        tweet_bot(text_data)
    except Exception as e:
        print(e, 'ツイッターでエラーが起きてます')
        pass
    exit(0)

#毎朝お金を入れる。
def input_money():
    driver = webdriver.Chrome('./chromedriver')
    for i in range(3):
        print("b")
        try:
            with open('../../../password.binaryfile', 'rb') as web:
                data = pickle.load(web)
            web.close
            driver.get('https://ib.mbrace.or.jp/') 
            driver.implicitly_wait(60) # 秒
            time.sleep(3)
            print(driver.current_window_handle)
            number = driver.find_element("name", "memberNo")
            number.send_keys(data[0])
            password = driver.find_element("name", "pin")
            password.send_keys(data[1])
            confirm_password = driver.find_element("name", "authPassword")
            confirm_password.send_keys(data[2])
            button = driver.find_element("id", "loginButton")
            button.click()

            time.sleep(3)
            handle_array = driver.window_handles
            driver.switch_to.window(handle_array[1])
            
            money_push = driver.find_element(By.CLASS_NAME, "menu-item-has-children")
            money_push.click()
            time.sleep(1)
            money_push_01 = driver.find_element("id", "list01")
            money_push_01.click()
            time.sleep(1)
            how_much_money = driver.find_element("id", "chargeInstructAmt")
            how_much_money.clear()
            how_much_money.send_keys("10")
            time.sleep(1)
            how_much_money_password = driver.find_element("id", "chargeBetPassword")
            how_much_money_password.clear()
            how_much_money_password.send_keys(data[3])
            time.sleep(1)
            how_much_money_button = driver.find_element("id", "executeCharge")
            how_much_money_button.click()

            time.sleep(1)
            how_much_money_ok_button = driver.find_element("id", "ok")
            how_much_money_ok_button.click()

            
        except Exception as e:
            print(e)
            driver.quit()
            print(traceback.format_exc())
            pass
        finally:
            time.sleep(3)
            driver.quit()

            
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
    schedule.every().days.at("22:00").do(day_notification)
    schedule.every().days.at("7:00").do(input_money)
    while True:
        schedule.run_pending()
        time.sleep(1)



if __name__ == '__main__':
    a = [[[1,5], [2,6], 3, 10], [[], 5, 10]]
    input_money()