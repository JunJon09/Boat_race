#レースの予測する
#艇番 名前 全国2連率 全国勝率 当地勝率 当地2連率 モータ2連率 ボード2連率 級 展示タイム スタート展示 天気 着順

from classification import dataSplit
from scikit_learn import sckit_learn
import pickle

def predict(text):
  print('predictがStart!')
  # x_train, x_test, y_train, y_test, y_odds = dataSplit(text)
  # with open('../../binaryfile/x_train.binaryfile', 'wb') as web:
  #           pickle.dump(x_train, web)
  # web.close
  # with open('../../binaryfile/y_train.binaryfile', 'wb') as web:
  #           pickle.dump(y_train, web)
  # web.close
  # with open('../../binaryfile/x_test.binaryfile', 'wb') as web:
  #           pickle.dump(x_test, web)
  # web.close
  # with open('../../binaryfile/y_test.binaryfile', 'wb') as web:
  #           pickle.dump(y_test, web)
  # web.close
  # with open('../../binaryfile/odds.binaryfile', 'wb') as web:
  #           pickle.dump(y_odds, web)
  # web.close

  
  with open('../../binaryfile/x_train.binaryfile', 'rb') as web:
    x_train = pickle.load(web)
  web.close
  with open('../../binaryfile/x_test.binaryfile', 'rb') as web:
    x_test = pickle.load(web)
  web.close
  with open('../../binaryfile/y_train.binaryfile', 'rb') as web:
    y_train = pickle.load(web)
  web.close
  with open('../../binaryfile/y_test.binaryfile', 'rb') as web:
    y_test = pickle.load(web)
  web.close
  with open('../../binaryfile/odds.binaryfile', 'rb') as web:
    y_odds = pickle.load(web)
  web.close


  y_test, y_pred= sckit_learn(x_train, x_test, y_train, y_test)
  
  return  y_test, y_pred, y_odds, x_train

  

