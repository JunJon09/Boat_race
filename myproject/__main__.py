#大元
from predicting import predict
from recovery_rate import recovery_rate
import pickle
if __name__ == '__main__':

    s = input('分類:"1", 回帰:"2": ')
    #予測
    y_test, y_pred, y_odds, x_train = predict('../binaryfile/boat01.binaryfile', s)
    #回収率計算
    recovery_rate(y_test, y_pred, y_odds, x_train)

    #実際に購入する。
    
    





    
   
    
     