#ランダムフォレストを使って学習

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LinearRegression


def sckit_learn(x_train, x_test, y_train, y_test):

    # clf = RandomForestClassifier(max_depth=30, n_estimators=30, random_state=42)

    # clf.fit(x_train, y_train.values.ravel())
    reg_lr = LinearRegression()
    reg_lr.fit(x_train, y_train.values.ravel())
    y_pred = reg_lr.predict(x_test)
    return y_test, y_pred