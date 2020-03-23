import pandas as pd
from flask import Flask, escape, request
from flask_cors import CORS, cross_origin
import time

from extractServiceInfo import extractServiceInfo
from extractWords import getWords
from words import addWordDictToSession, getWordDictFromSession
from utils import tag_mail

app = Flask(__name__)
CORS(app)


@cross_origin
@app.route('/analytics/mail', methods=['POST'])
def mailAnalytics():
    df = pd.DataFrame(request.json['received'])
    df['cat'] = df.headers.apply(tag_mail)
    res = extractServiceInfo(df)

    # print(request.json['sent'])
    # print(pd.DataFrame(request.json['sent']))
    addWordDictToSession(request.json['token'], getWords(
        pd.DataFrame(request.json['sent'])))

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
    words = getWordDictFromSession(request.args.get('token'))
    print(words)
    return {"words": words}
