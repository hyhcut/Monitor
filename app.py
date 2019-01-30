from flask import Flask,render_template
from Connect import link

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')
    # win = link('192.168.70.204', 'administrator', 'LRTabc123.')
    # win.test()
    # return 'Hello World!'


if __name__ == '__main__':
    app.run()
