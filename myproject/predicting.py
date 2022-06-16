#レースの予測する
#艇番 名前 全国2連率 全国勝率 当地勝率 当地2連率 モータ2連率 ボード2連率 級 展示タイム スタート展示 天気 着順

from classification import dataSplit
from algorithm import kreas_neuralnetwork

def predict():
  print('predictがStart!')
  text = 'boat-tsu_two.binaryfile'
  x_train, x_test, y_train, y_test = dataSplit(text)
  
  kreas_neuralnetwork( x_train, x_test, y_train, y_test)
  
  
