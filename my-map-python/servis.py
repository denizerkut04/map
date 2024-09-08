from flask import Flask
from flask_cors import CORS

from turkiye import data_turkiye

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

@app.route('/api')
def hello_world():  # put application's code here
    # loop 1 to 10
    mesaj = "Hello Deniz!"
    for i in range(1, 11):
        mesaj += str(i)
    return mesaj

@app.route('/api/harita')
def hello_harita():  # put application's code here
    return data_turkiye


