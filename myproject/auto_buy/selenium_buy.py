import time
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pickle
def selenium_buy(result, stage, race):
    driver = webdriver.Chrome()  #WEBブラウザの起動

    driver.get('https://ib.mbrace.or.jp/') 
    try:
        with open('../../../password.binaryfile', 'rb') as web:
            data = pickle.load(web)
    except Exception as e:
        print(e)
        return e
    time.sleep(1)
    number = driver.find_element("name", "memberNo")
    number.send_keys(data[0])
    password = driver.find_element("name", "pin")
    password.send_keys(data[1])
    confirm_password = driver.find_element("name", "authPassword")
    confirm_password.send_keys(data[2])
    button = driver.find_element("id", "loginButton")
    button.click()

    time.sleep(10)
    handle_array = driver.window_handles
    driver.switch_to.window(handle_array[1])
    stage = str(stage)
    stage = "jyo"+stage.zfill(2)
    button = driver.find_element("id", stage)
    button.click()

    time.sleep(5)
    race = str(race)
    race = "selRaceNo" + race.zfill(2)
    race = driver.find_element("id", race)
    race.click()


    rank = []
    print(result)
    for i, number in enumerate(result):
        if number == 1:
            rank.append(i+1)

    for i, number in enumerate(result):
        if number == 2:
            rank.append(i+1)
    
    for i, number in enumerate(result):
        if number == 3:
            rank.append(i+1)
    print(rank)
    #二連単
    two_win = driver.find_element("id", "betkati3")
    two_win.click()

    time.sleep(3)

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

    time.sleep(3)
    #単勝
    one_win = driver.find_element("id", "betkati1")
    one_win.click()
    first_text = "regbtn_" + str(rank[0]) + "_1"
    first_text = driver.find_element("id", first_text)
    first_text.click()
    Bet_append = driver.find_element("id", "regAmountBtn")
    Bet_append.click()

    voting = driver.find_elements(By.CLASS_NAME, "btnSubmit ")
    print(voting)
    #
    #driver.find_element_by_xpath('//*[@id="betList"]/div[3]/div[3]')
    voting[0].click()
    
    time.sleep(2)
    check_money = driver.find_element("id", "amount")
    check_money.send_keys("200")

    voting_password = driver.find_element("id", "pass")
    voting_password.send_keys(data[3])


    submitBet =  driver.find_element("id", "submitBet")
    submitBet.click()
    time.sleep(3)
    okButton = driver.find_element("id", "ok")
    okButton.click()
    time.sleep(10)