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
from flask import Flask, render_template, jsonify, send_from_directory
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

# you can specify the base template by: index.html is the default template
singleview = singleview(app, base_template='index.html')


# routes
#######################################################

@app.route('/', no_preload=True, no_ajax_socket_load=True)
def index():
	return render_template('index.html')

@app.route('/<path:path>', route_exclude=True)
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

***BREAKS THINGS***
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

this is how the index template is setup

```html
<body>
	<!-- links; not required -->
	<ul>
		<li><a href="##">home</a></li>
		<li><a href="##1">1</a></li>
		<li><a href="##2">2</a></li>
		<li><a href="##3/pipskweak">3</a></li>
	</ul>

	<!-- content; leave it EXACTLY like this -->
	<div id="singleview-content">
		{% if preload_content is defined %}
			{% autoescape false %}
				{{ preload_content }}
			{% endautoescape %}
		{% endif %}
	</div>

	<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
	{% if content_method == 'ajax' %}
		<script type="text/javascript" src="{{url_for('static', filename='ajax.js')}}"></script>
	{% elif content_method == 'socketio' %}
		<script type="text/javascript" src="http://cdnjs.cloudflare.com/ajax/libs/socket.io/1.3.6/socket.io.min.js"></script>
		<script type="text/javascript" src="{{url_for('static', filename='socketio.js')}}"></script>
	{% endif %}
</body>
```

> note it doesn't matter how your custom views are rendering, it'll just pop it into the `div` with the id `singleview-content`

## href-ing the shit out of your web app
So, by now you must be wondering how to actually reference and link between pages.

```html
<!-- goes to index -->
<a href="##">home</a>
```

*`url_for()` also works*
```html
<!-- goes to the url of route_1 -->
<a href="##{{url_for('route_1')}}">1</a>
<!-- note the two leading hashtags -->
```

Just reference all **internal** links with **`##`** before. This way, js can capture it.

You can decide whether or not you want to omit the leading `/` from your `href` attributes, singleview_flask takes it into account either way.

##### examples

- `##hello` &rarr; `example.com/hello`

- `##/hello` &rarr; `example.com/hello`

- `##hello/name` &rarr; `example.com/hello/name`

#### why lead with `##`?
Good question, it's still fairly standard when it comes to a URL, meaning that it isn't going to chuck a tantrum if the js doesn't load properly, it may not work, but it won't scream at you.

## what else do I need to do to get this sucker working?
Firstly, you'll need to create a folder named `static`, where you can pop all the necessary files, like css, js, and images. Think of it like your assets folder.

You'll need to download `ajax.js` and `socketio.js` from the `data/scripts` folder of this repo ([here is a link](https://github.com/harryparkdotio/flask-singleview)), and put it into the static folder in the root directory.

You'll also need a `templates` folder in your root directory, containing the templates your project will use. It's a good idea to check out the template in the `data/templates` folder of this repo ([here is a link](https://github.com/harryparkdotio/flask-singleview)) to get a basis from, or to use.

Otherwise, here is what you'll need to add to the bottom of your webpage to load the required javascript correctly.

```html
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
{% if content_method == 'ajax' %}
	<script type="text/javascript" src="{{url_for('static', filename='ajax.js')}}"></script>
{% elif content_method == 'socketio' %}
	<script type="text/javascript" src="http://cdnjs.cloudflare.com/ajax/libs/socket.io/1.3.6/socket.io.min.js"></script>
	<script type="text/javascript" src="{{url_for('static', filename='socketio.js')}}"></script>
{% endif %}
```

If you are confused, please check out the example, it might make a bit more sense.

#### quirk 1
##### double render
Double render, think of it like `render_template()` inception, because thats exactly what it is.

> `render_template(render_template())` &larr; general gist of it

to prevent this (it shouldn't occur, unless you're doing weird shit. Let me know if you are though, I'd be interested in hearing about it)

add `route_exclude=True` as a param of the `@app.route()` decorator.

```python
@app.route('/func', route_exclude=True)
def func():
	return render_template('template.html')
```

#### quirk 2
If you are choosing to go the AJAX route (pun intended), then you really, really, really, don't want to route **anything** to the route `/page`. This is due to the fact that flask_singleview is using it to send pages to the client.

## weird things you may or may not find handy
this won't allow for preloading, it will still allow the user to access it directly, it just won't show anything but the standard `index.html` page.
```python
@app.route('/func', no_preload=True)
def func():
	return render_template('template.html')
```

Basically the same thing as above, but opposite, only shows content if accessed directly, not through AJAX or socketio (clicked an internal link).
```python
@app.route('/func', no_ajax_socket_load=True)
def func():
	return render_template('template.html')
```

Now this one is a tad odd, and useful if you just want to return the function as normal. This prevents double render, a quirk.
```python
@app.route('/func', route_exclude=True)
def func():
	return render_template('template.html')
```
