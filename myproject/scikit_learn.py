#ランダムフォレストを使って学習

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def sckit(x_train, x_test, y_train, y_test):

    clf = RandomForestClassifier(max_depth=30, n_estimators=30, random_state=42)

    clf.fit(x_train, y_train)
    print(x_train, x_test)
    y_pred = clf.predict(x_test)
    print(y_pred)
    accuracy = accuracy_score(y_test, y_pred)
    print('Accuracy: {}'.format(accuracy))