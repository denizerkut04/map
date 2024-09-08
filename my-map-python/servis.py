from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():  # put application's code here
    # loop 1 to 10
    mesaj = "Hello Deniz!"
    for i in range(1, 11):
        mesaj += str(i)
    return mesaj

@app.route('/harita/')
def hello_harita():  # put application's code here
    map = dict()
    map["name"] = "deniz"
    map["surname"] = "yılmaz"
    return map

