from flask import Flask
from flask import url_for
from flask import render_template 

app = Flask(__name__)

@app.route('/')
def index():
    return 'index'

@app.route('/test')
def app_test():
    test = ['hello' for i in range(10000)]
    return 'hello'+ f"{['hello' for i in range(10000)]}"

@app.route('/hello')
def hello():
    return 'hello'

with app.test_request_context():
    print(url_for('index'))



