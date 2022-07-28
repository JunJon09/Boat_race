#レースの予測する
#艇番 名前 全国2連率 全国勝率 当地勝率 当地2連率 モータ2連率 ボード2連率 級 展示タイム スタート展示 天気 着順

from algorithm import algorithm
import pickle

def predict():
  print('predictがStart!')
  text = 23
  text = str(text)
  x_train_text = "../../binaryfile/x_train_" + text.zfill(2) + ".binaryfile"
  y_train_text = "../../binaryfile/y_train_" + text.zfill(2) + ".binaryfile"
  x_test_text = "../../binaryfile/x_test_" + text.zfill(2) + ".binaryfile"
  y_test_text = "../../binaryfile/y_test_" + text.zfill(2) + ".binaryfile"
  odds_text = "../../binaryfile/odds_" + text.zfill(2) + ".binaryfile"
  
  with open(x_train_text, 'rb') as web:
    x_train = pickle.load(web)
  web.close
  with open(x_test_text, 'rb') as web:
    x_test = pickle.load(web)
  web.close
  with open(y_train_text, 'rb') as web:
    y_train = pickle.load(web)
  web.close
  with open(y_test_text, 'rb') as web:
    y_test = pickle.load(web)
  web.close
  with open(odds_text, 'rb') as web:
    y_odds = pickle.load(web)
  web.close


  y_test, y_pred= algorithm(x_train, x_test, y_train, y_test)
  
  return  y_test, y_pred, y_odds, x_train

  

