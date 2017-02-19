from flask import render_template
from functools import wraps
import re, base64

# https://ains.co/blog/things-which-arent-magic-flask-part-1.html
# https://ains.co/blog/things-which-arent-magic-flask-part-2.html
class singleview:
	def __init__(self, app, socketio):
		self.app = app
		self.socketio = socketio
		app.route = self.route
		self.routes = []

	@staticmethod
	def build_route_pattern(route):
		# gets the name of the variable (surrounded by `< * >`)
		route_regex = re.sub(r'(<\w+>)', r'(?P\1.+)', route)
		# compiles it into a glorious regex
		return re.compile("^{}$".format(route_regex))

	def route(self, rule, no_preload=False, no_socket_load=False, **options):
		def decorator(f):
			@wraps(f)
			def decorated_function(socket_call=False, *args, **kwargs):
				if socket_call == False:
					if no_preload:
						return render_template('index.html')
					else:
						return render_template('index.html', preload_content=f(*args, **kwargs))
				else:
					if no_socket_load:
						return ''
					else:
						return f(*args, **kwargs)
			self.routes.append((self.build_route_pattern(rule), decorated_function))
			# this is exactly how the `@app.route()` decorator does its thing
			self.app.add_url_rule(rule, decorated_function.__name__, decorated_function, **options)

			return decorated_function
		return decorator

	def get_route_match(self, path):
		# matches the route with the
		for route_pattern, view_function in self.routes:
			m = route_pattern.match(path)
			if m:
				return m.groupdict(), view_function
		return None

	def serve(self, path):
		# strips the leading `/` and adds it, this is just for preventing errors
		path = '/' + path.lstrip('/')
		# matches the serve path with a path in the list
		route_match = self.get_route_match(path)
		if route_match:
			kwargs, view_function = route_match
			# socketio emits the page
			self.socketio.emit('page', base64.b64encode(view_function(socket_call=True, **kwargs)), namespace='/page')
		else:
			return 404
