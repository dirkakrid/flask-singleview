# flask-singleview
A flask micro extension for building *single-view* web apps.

[check out the docs](https://harryparkdotio.github.io/flask-singleview/)

### initial setup
```python
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
from flask_singleview import singleview
import requests, json, base64

app = Flask(__name__)
app.threaded = True

socketio = SocketIO(app)
singleview = singleview(app, socketio)

#######################################################
# socketio

@socketio.on('get page', namespace='/page')
def socket_page(data):
	singleview.serve(data['page'])

#######################################################
# routes

@app.route('/1')
def route_1():
	values = {"data": "this is page 1"}
	return render_template('default.html', **values)

#######################################################

if __name__ == "__main__":
	socketio.run(app, port=5000, debug=True)
```
