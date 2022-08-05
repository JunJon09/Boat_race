from classification import dataSplit
import pickle

def main():
    text = 8
    text = str(text)
    boat_text = "../../binaryfile/boat" + text.zfill(2) + ".binaryfile"
    x_train, x_test, y_train, y_test, y_odds = dataSplit(boat_text)
    x_train_text = "../../binaryfile/x_train_" + text.zfill(2) + ".binaryfile"
    y_train_text = "../../binaryfile/y_train_" + text.zfill(2) + ".binaryfile"
    x_test_text = "../../binaryfile/x_test_" + text.zfill(2) + ".binaryfile"
    y_test_text = "../../binaryfile/y_test_" + text.zfill(2) + ".binaryfile"
    odds_text = "../../binaryfile/odds_" + text.zfill(2) + ".binaryfile"
    with open(x_train_text, 'wb') as web:
                pickle.dump(x_train, web)
    web.close
    with open(y_train_text, 'wb') as web:
                pickle.dump(y_train, web)
    web.close
    with open(x_test_text, 'wb') as web:
                pickle.dump(x_test, web)
    web.close
    with open(y_test_text, 'wb') as web:
                pickle.dump(y_test, web)
    web.close
    with open(odds_text, 'wb') as web:
                pickle.dump(y_odds, web)
    web.close


if __name__ == '__main__':
    main()