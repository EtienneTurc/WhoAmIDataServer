from flask import Flask, escape, request
from flask_cors import CORS, cross_origin
import time

from utils import tag_mail
from extractServiceInfo import extractServiceInfo

import pandas as pd

app = Flask(__name__)
CORS(app)

@cross_origin
@app.route('/analytics/mail', methods=['POST'])
def mailAnalytics():

    df = pd.DataFrame(request.json['received'])
    df['cat'] = df.headers.apply(tag_mail)
    res = extractServiceInfo(df)

    return res
