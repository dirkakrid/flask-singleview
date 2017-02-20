# flask-singleview
A flask micro extension for building *single-view* web apps.

based on [flask-socketio](https://flask-socketio.readthedocs.io/en/latest/) or AJAX, your choice.

[check out the docs](https://harryparkdotio.github.io/flask-singleview/)

[check flask_singleview on pip](https://pypi.python.org/pypi/flask_singleview/)

## installation
`pip install flask_singleview`

### initial setup
```python
from flask import Flask, render_template, jsonify
# only necessary if you are using socketio
from flask_socketio import SocketIO
from flask_singleview import singleview
import requests, json, base64

app = Flask(__name__)
app.threaded = True

# if you want to use socketio
socketio = SocketIO(app)
singleview = singleview(app, socketio)

# if you just want to use AJAX
singleview = singleview(app)


# routes
#######################################################

@app.route('/', no_preload=True, no_ajax_socket_load=True)
def index():
	return render_template('index.html')

@app.route('/<path:path>')
def static_files(path):
	return app.send_static_file(path)

#######################################################

...

#######################################################

if __name__ == "__main__":
	# if you want to use socketio
	socketio.run(app, port=5000, debug=True)
	# if you just want to use AJAX
	app.run(debug=True)
```
