import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pickle
from selenium.common.exceptions import NoSuchElementException
import traceback
import chromedriver_binary
import re

def selenium_buy(rank, stage, race):
    driver = webdriver.Chrome('./chromedriver')  #WEBブラウザの起動
    tmp = []
    one_money_value = {'01': 2.9, '02': 2.9, '03': 2.9, '04': 2.9, '05': 2.7, '06': 2.8, '07': 2.7, '08': 100, '09': 100, '10': 100, '11': 100, '12': 100, '13': 100, '14': 100, '15': 100, '16': 100, '17': 100, '18': 100, '19': 100, '20': 100, '21': 2.7, '22': 2.6, '23':2.8, '24': 100}
    sub_money_value = {'01': 1.7, '02': 2.4, '03': 2.0, '04': 2.1, '05': 2.2, '06': 1.7, '07': 1.6, '08': 100, '09': 100, '10': 100, '11': 100, '12': 100, '13': 100, '14': 100, '15': 100, '16': 100, '17': 100, '18': 100, '19': 100, '20': 100, '21': 2.3, '22': 1.5, '23':1.9, '24': 2.1}
    one_money = one_money_value[str(stage).zfill(2)]
    sub_money = sub_money_value[str(stage).zfill(2)]
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
            boat_stage = "jyo"+str(stage).zfill(2)
            button = driver.find_element("id", boat_stage)
            print(driver.current_window_handle)
            button.click()

            race = "selRaceNo" + str(race).zfill(2)
            print(driver.current_window_handle)
            #race = driver.find_element("id", race)
            
            # for i in handle_array:
            #     if driver.current_window_handle == i and i==0:
            #         driver.switch_to.window(handle_array[1])
            #         break
            #     if driver.current_window_handle == i and i==1:
            #             driver.switch_to.window(handle_array[0])
            #race.click()
            # time.sleep(5)
            # #二連単
            # two_win = driver.find_element("id", "betkati3")
            # two_win.click()


            # #1位のボタン
            # first_text = "regbtn_" + str(rank[0]) + "_1"
            # first_text = driver.find_element("id", first_text)
            # first_text.click()
            # #２位
            # second_text = "regbtn_" + str(rank[1]) + "_2"
            # second_text = driver.find_element("id", second_text)
            # second_text.click()
            
            # money = driver.find_element("id", "amount")
            # money.send_keys("1")
            # # mail.submit()
            # Bet_append = driver.find_element("id", "regAmountBtn")
            # Bet_append.click()
        
            time.sleep(3)
            money = driver.find_element("id", "amount")
            money.send_keys("1")
            for r in rank:
                if r[1] == 5: #単勝
                    one_win = driver.find_element("id", "betkati1")
                    one_win.click()
                    first_text = "regbtn_" + str(r[0]) + "_1"
                    first_text = driver.find_element("id", first_text)
                    first_text.click()
                    money_odds = driver.find_element(By.CLASS_NAME, "oddsBox").text
                    money_odds = money_odds[3:]
                    print(money_odds)
                    money_odds = float(money_odds)
                    time.sleep(3)
                    if 1.0 <= money_odds and one_money <= money_odds:
                        Bet_append = driver.find_element("id", "regAmountBtn")
                        Bet_append.click()
                        tmp.append(r[0])
                        tmp.append(5)              
                    
                elif r[1] == 6: #複勝
                    sub_win = driver.find_element("id", "betkati2")
                    sub_win.click()
                    first_text = "regbtn_" + str(r[0]) + "_1"
                    first_text = driver.find_element("id", first_text)
                    first_text.click()
                    money_odds = driver.find_element(By.CLASS_NAME, "oddsBox").text
                    money_odds = money_odds[3:]
                    one = money_odds[:3]
                    two = money_odds[4:]
                    print(one)
                    print(two)
                    money_odds = (float(one) + float(two))/2
                    if 1.0 <= money_odds and  sub_money <= money_odds:
                        Bet_append = driver.find_element("id", "regAmountBtn")
                        Bet_append.click()
                        tmp.append(r[0])
                        tmp.append(6)
            voting = driver.find_elements(By.CLASS_NAME, "btnSubmit ")
            #
            #driver.find_element_by_xpath('//*[@id="betList"]/div[3]/div[3]')
            voting[0].click()

            time.sleep(3)
            
            value = int(len(tmp) / 2 * 100)
            print(value)
            check_money = driver.find_element("id", "amount")
            check_money.send_keys(value)

            voting_password = driver.find_element("id", "pass")
            voting_password.send_keys(data[3])


            submitBet = driver.find_element("id", "submitBet")
            submitBet.click()

            time.sleep(3)
            okButton = driver.find_element("id", "ok")
            okButton.click()

        except Exception as e:
            print(e)
            driver.quit()
            print(traceback.format_exc())
            pass
        finally:
            time.sleep(3)
            driver.quit()
            a = []
            buy = []
            if len(tmp) != 0:
                for i, t in enumerate(tmp):
                    a.append(t)
                    if i % 2 == 1:
                        buy.append(a)
                        a = []    
            break

    else:
        raise ValueError("購入部分でエラーが発生しました。")
    print(buy)
    return buy

if __name__ == '__main__':
    rank_1 = [[2, 5],[1, 6]]
    buy = selenium_buy(rank_1, 1, 5)
    buy.append(1)
    buy.append(12)
    print(buy)

    