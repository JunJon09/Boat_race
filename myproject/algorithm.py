#色々なニューラルネットワークを試す場所

#from keras.models import Sequential
#from keras.layers import Dense, Dropout
#from tensorflow.keras.callbacks import EarlyStopping

#TensorFlowまたはCNTK，Theano上で実行可能な高水準のニューラルネットワークライブラリ
def kreas_neuralnetwork(x_train, x_test, y_train, y_test):
  print('kreas_neuralnetworkがStrat!')
  print(x_train)
  # model = Sequential()
  # model.add(Dense(132, input_shape=(x_train.shape[1],), activation='relu'))
  # model.add(Dropout(0.36))
  # model.add(Dense(200, activation='relu'))
  # model.add(Dropout(0.49))
  # model.add(Dense(200, activation='relu'))
  # model.add(Dropout(0.49))
  # model.add(Dense(y_train.shape[1], activation='softmax'))
  # model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
  
  # early_stopping = EarlyStopping(patience=10, verbose=1)
  # model.fit(x_train, y_train, batch_size=50, verbose=0, epochs=100, validation_split=0.1, callbacks=[early_stopping])
  
  # score = model.evaluate(x_test, y_test, verbose=1)
  # print("Test loss:",score[0])
  # print("Test accuracy:",score[1])
  # print('Finish')
  # print(score)