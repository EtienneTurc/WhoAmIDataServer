from flask import Flask, escape, request
from flask_cors import CORS, cross_origin
import time

app = Flask(__name__)
CORS(app)

@cross_origin
@app.route('/analytics', methods=['POST'])
def simulate_long_request():
    print(request.json)
    return {"result":"non merci, bisous"}