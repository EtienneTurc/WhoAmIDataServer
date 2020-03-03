from flask import Flask, escape, request
from flask_cors import CORS, cross_origin
import time

from utils import tag_mail
from str_mails import lydia

import pandas as pd

app = Flask(__name__)
CORS(app)

@cross_origin
@app.route('/analytics', methods=['POST'])
def simulate_long_request():
    print(request.json)

    df = pd.read_json({request.json}, encoding = 'utf-8')
    df['cat'] = df.headers.apply(tag_mail)

    res = lydia(df)

    

    return res #{"result":"non merci, bisous"}


print(simulate_long_request())