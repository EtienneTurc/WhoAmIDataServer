import pandas as pd
from extractServiceInfo import extractServiceInfo
from utils import tag_mail
from flask import Flask, escape, request
from flask_cors import CORS, cross_origin
import time

import redis
r = redis.Redis()


app = Flask(__name__)
CORS(app)


@cross_origin
@app.route('/analytics/mail', methods=['POST'])
def mailAnalytics():
    df = pd.DataFrame(request.json['received'])
    df['cat'] = df.headers.apply(tag_mail)
    res = extractServiceInfo(df)

    return res


@cross_origin
@app.route('/analytics/drive', methods=['POST'])
def driveAnalytics():
    df = pd.DataFrame(request.json['received'])
    df['cat'] = df.headers.apply(tag_mail)
    res = extractServiceInfo(df)

    return res


@cross_origin
@app.route('/analytics/words', methods=['GET'])
def words():
    """
    Returns list of words in the session, then deletes them.
    """
    wordList = []
    while(r.llen("session") != 0):
        wordList.append(r.rpop("session").decode("utf-8"))
    return {"words": wordList}
