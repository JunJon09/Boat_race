#レースの予測する
#艇番 名前 全国2連率 全国勝率 当地勝率 当地2連率 モータ2連率 ボード2連率 級 展示タイム スタート展示 天気 着順

from classification import dataSplit
from scikit_learn import sckit_learn

def predict(text, s):
  print('predictがStart!')
  x_train, x_test, y_train, y_test, y_odds = dataSplit(text)
  y_test, y_pred= sckit_learn(x_train, x_test, y_train, y_test, s)
  
  return  y_test, y_pred, y_odds, x_train

  

