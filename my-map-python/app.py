from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    # loop 1 to 10
    mesaj = "Hello Deniz!"
    for i in range(1, 11):
        mesaj += str(i)

    return mesaj


if __name__ == '__main__':
    app.run()
