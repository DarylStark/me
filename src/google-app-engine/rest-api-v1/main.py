#!/usr/bin/env python3
from flask import Flask

app = Flask(__name__)

@app.route('/<path:path>')
def say_hello(path = '#'):
    return 'You\'ve reached the API service with path {path}'.format(path = path)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8001, debug=True)
