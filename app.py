from flask import Flask, request, render_template
from Connect import link
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')
    # win = link('192.168.70.204', 'administrator', 'LRTabc123.')
    # win.test()
    # return 'Hello World!'


@app.route('/test_connect', methods=['GET', 'POST'])
def test_connect():
    if request.method == 'POST':
        address = request.json.get('address')
        username = request.json.get('username')
        password = request.json.get('password')
        win = link(address, username, password, None)
        win.test()
        return 'success'


@app.route('/status', methods=['GET', 'POST'])
def status():
    if request.method == 'POST':
        address = request.json.get('address')
        username = request.json.get('username')
        password = request.json.get('password')
        win = link(address, username, password, None)
        win.test()
        cpu = win.get_cpu()
        mem = win.get_mem()
        return json.dumps({'cpu': cpu, 'mem': mem})


if __name__ == '__main__':
    app.run()
