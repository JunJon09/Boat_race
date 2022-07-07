from email import message
import requests
import pickle
import schedule
import time
import matplotlib.pyplot as plt






def a():
    pass
        

if __name__ == '__main__':
    all_money = []
    with open('../binaryfile/money.binaryfile', 'wb') as web:
        pickle.dump(all_money, web)
        web.close
    with open('../binaryfile/money.binaryfile', 'rb') as web:
        all_money = pickle.load(web)
        print(all_money)
        web.close
    figure, ax = plt.subplots() #グラフの定義
    x = [i+1 for i in range(len(all_money))]
    y = all_money
    ax.plot(x,y) 
    figure.savefig('../PLT/test.jpg')
    message = "a"
    

    