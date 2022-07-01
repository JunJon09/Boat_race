#ランダムフォレストを使って学習

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LinearRegression
import pandas as pd

def sckit_learn(x_train, x_test, y_train, y_test):
    #分類
    # clf = RandomForestClassifier(max_depth=30, n_estimators=30, random_state=42)
    # clf.fit(x_train, y_train.values.ravel())
    # y_pred = clf.predict(x_test)
    #回帰
    reg_lr = LinearRegression()
    reg_lr.fit(x_train, y_train.values.ravel())
    y_pred = reg_lr.predict(x_test)
    #標準化偏回帰係数を求めてる
    coef_df = pd.DataFrame(reg_lr.coef_,x_train.columns)
    # print(coef_df)
    return y_test, y_pred