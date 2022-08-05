from pydoc import TextDoc
from matplotlib.pyplot import text
import pickle
import tweepy
# 取得したアクセスキーたちをセット。
def tweet_bot(message="エラー"):
    text = '../../../twitter_info.binaryfile'
    with open(text, 'rb') as web:
        data = pickle.load(web)
    web.close
    ck= data[0]
    cs= data[1]
    at= data[2]
    ats= data[3]
    auth = tweepy.Client(consumer_key=ck, consumer_secret=cs, access_token=at, access_token_secret=ats)
    auth.create_tweet(text=message)
    print("ee")