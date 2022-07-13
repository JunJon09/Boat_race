import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pickle
from selenium.common.exceptions import NoSuchElementException
import traceback

def selenium_buy(rank, stage, race):
    for i in range(3):
        try:
            with open('../../../password.binaryfile', 'rb') as web:
                data = pickle.load(web)
            web.close
            driver = webdriver.Chrome()  #WEBブラウザの起動
            driver.get('https://ib.mbrace.or.jp/') 
            driver.implicitly_wait(60) # 秒
            # time.sleep(5)
            print(driver.current_window_handle)
            number = driver.find_element("name", "memberNo")
            number.send_keys(data[0])
            password = driver.find_element("name", "pin")
            password.send_keys(data[1])
            confirm_password = driver.find_element("name", "authPassword")
            confirm_password.send_keys(data[2])
            button = driver.find_element("id", "loginButton")
            button.click()

            # time.sleep(3)
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
            #二連単
            two_win = driver.find_element("id", "betkati3")
            two_win.click()


            #1位のボタン
            first_text = "regbtn_" + str(rank[0]) + "_1"
            first_text = driver.find_element("id", first_text)
            first_text.click()
            #２位
            second_text = "regbtn_" + str(rank[1]) + "_2"
            second_text = driver.find_element("id", second_text)
            second_text.click()
            
            money = driver.find_element("id", "amount")
            money.send_keys("1")
            # mail.submit()
            Bet_append = driver.find_element("id", "regAmountBtn")
            Bet_append.click()

            # time.sleep(5)

            #単勝
            one_win = driver.find_element("id", "betkati1")
            one_win.click()
            first_text = "regbtn_" + str(rank[0]) + "_1"
            first_text = driver.find_element("id", first_text)
            first_text.click()
            Bet_append = driver.find_element("id", "regAmountBtn")
            Bet_append.click()

            voting = driver.find_elements(By.CLASS_NAME, "btnSubmit ")
            #
            #driver.find_element_by_xpath('//*[@id="betList"]/div[3]/div[3]')
            voting[0].click()

            time.sleep(3)
            
            check_money = driver.find_element("id", "amount")
            check_money.send_keys("200")

            voting_password = driver.find_element("id", "pass")
            voting_password.send_keys(data[3])


            submitBet = driver.find_element("id", "submitBet")
            submitBet.click()

            # time.sleep(10)
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
            break

    else:
        raise ValueError("購入部分でエラーが発生しました。")

if __name__ == '__main__':
    selenium_buy([1,2,3], 1, 2)

    