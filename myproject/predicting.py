from statistics import mode
import pandas as pd
import pickle
import numpy as np

from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop
from keras.optimizers import Adam

from tensorflow.keras.callbacks import EarlyStopping

def predict():
  with open('boat-tsu_two.binaryfile', 'rb') as web:
    boat_tsu = pickle.load(web)
  
  list_std = ['艇番', '全国2連率', '全国勝率', '当地勝率', '当地2連率', 'モータ2連率', 'ボード2連率', '級','展示タイム', 'スタート展示', '天気', 'レーサ番号']
  
  result_std = ['順位']
  
  y_label = ["1.0", "2.0", "3.0", "4.0", "5.0", "6.0"]
  x, y = split_train_test(boat_tsu, list_std, result_std)
  
  x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
  print(y_train)
  y_train = one_hot_encode(y_train, y_label)
  y_test = one_hot_encode(y_test, y_label)
  print(y_train)
  model = Sequential()
  model.add(Dense(132, input_shape=(x_train.shape[1],), activation='relu'))
  model.add(Dropout(0.36))
  model.add(Dense(200, activation='relu'))
  model.add(Dropout(0.49))
  model.add(Dense(200, activation='relu'))
  model.add(Dropout(0.49))
  model.add(Dense(y_train.shape[1], activation='softmax'))
  model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
  
  early_stopping = EarlyStopping(patience=10, verbose=1)
  model.fit(x_train, y_train, batch_size=50, verbose=0, epochs=100, validation_split=0.1, callbacks=[early_stopping])
  
  score = model.evaluate(x_test, y_test, verbose=1)
  print("Test loss:",score[0])
  print("Test accuracy:",score[1])
  print('Finish')
  print(score)
  
 
#訓練データとテストデータをわける。
def split_train_test(boat_tsu, list_std, result_std):
  learn = pd.DataFrame(index=[])
  result = pd.DataFrame(index=[])
  for n in boat_tsu:
    for i in n:
      a = i.pop(-1)
      b = i
      tmp_learn =  pd.Series(b, index=list_std)
      tmp_result = pd.Series(a, index=result_std)
      learn = learn.append(tmp_learn, ignore_index=True)
      result = result.append(tmp_result, ignore_index=True)
  
  return learn, result

def one_hot_encode(y_data,y_label):
    results = np.zeros((y_data.shape[0], len(y_label)))
    for n in range(y_data.shape[0]):
        result = y_data.iat[n,0].astype(str)
        index = y_label.index(result)
        results[n, index] = 1
    return results
  
