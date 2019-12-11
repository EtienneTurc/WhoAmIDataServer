from flask import Flask, escape, request
from flask_cors import CORS, cross_origin
import time

app = Flask(__name__)
CORS(app)

@cross_origin
@app.route('/analytics')
def simulate_long_request():
    time.sleep(10)
    return {"result":"this is the result of a long request"}