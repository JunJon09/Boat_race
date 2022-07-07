import requests
import pickle
def LINENotifyBot(message, file=0):
    url = "https://notify-api.line.me/api/notify"
    try:
        with open('../../../access_token.binaryfile', 'rb') as web:
            data = pickle.load(web)
        web.close
    except Exception as e:
        print(e)
        return e
    access_token = data[0]
    headers = {'Authorization': 'Bearer ' + access_token}
    payload = {'message': message}
    if file == 0:
        r = requests.post(url, headers=headers, params=payload,)
    else:
        files = {'imageFile': open(file, 'rb')}
        r = requests.post(url, headers=headers, params=payload, files=files,)
    