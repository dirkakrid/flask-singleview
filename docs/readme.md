# installation

```zsh
git clone https://github.com/harryparkdotio/flask-singleview.git
```

*in app.py*

```python
from flask_singleview import singleview
singleview = singleview(app, socketio)
```

# documentation

## initial setup
```python
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
from flask_singleview import singleview
import requests, json, base64

app = Flask(__name__)
app.threaded = True

socketio = SocketIO(app)
singleview = singleview(app, socketio)

# socketio
#######################################################

@socketio.on('get page', namespace='/page')
def socket_page(data):
	singleview.serve(data['page'])

#######################################################

# routes

#######################################################

if __name__ == "__main__":
	socketio.run(app, port=5000, debug=True)
```

> note, this is almost identical to that of the `app.py` file

## declaring a route
```python
@app.route('/1')
def route_1():
	values = {"data": "this is page 1<br><a href='##2'>page 2</a>"}
	return render_template('default.html', **values)
```

*Adding a variable in the url still works.*
```python
@app.route('/hello/<name>')
def hello(name):
	return render_template('default.html', name=name)
```

*But declaring the variable type doesn't.*
```python
@app.route('/hello/<int:name>') # nope --> `int:`
def hello(name):
	return render_template('default.html', name=name)
```

*And multiple routes on the same function doesn't work either. You'll just get errors*
```python
@app.route('/hello/<name>')
@app.route('/hello/', defaults={'name': 'pipskweak'})
def hello(name):
	return render_template('default.html', name=name)
```

*But standard options for routes do work!*
```python
@app.route('/hello', methods=['GET', 'POST'])
def hello(name):
	return render_template('default.html', name=name)
```

## route modification
disabling socketio (preventing unnecessary calls)

```python
@app.route('/', no_socket_load=True)
def index():
	template_vars = {}
	return render_template('index.html', **template_vars)
```

disabling content preload (preventing double render)
```python
@app.route('/', no_preload=True)
def index():
	template_vars = {}
	return render_template('index.html', **template_vars)
```

## templating
The default template which everything is inserted into is `index.html`.

This is how flask singleview works as a basic overview):

```python
if accessed_by == 'socketio':
	return render_template(template, values)
elif accessed_by == 'flask_route':
	preload_content = render_template(template, values)
	return render_template('index.html', preload_content=preload_content)
```
