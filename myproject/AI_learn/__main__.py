#大元
from predicting import predict
from recovery_rate import recovery_rate
import pickle
if __name__ == '__main__':

    #予測
    y_test, y_pred, y_odds, x_train = predict()
    #回収率計算
    recovery_rate(y_test, y_pred, y_odds, x_train)

     