from flask import render_template, jsonify
from functools import wraps
import re, base64

# https://ains.co/blog/things-which-arent-magic-flask-part-1.html
# https://ains.co/blog/things-which-arent-magic-flask-part-2.html
class singleview:
	def __init__(self, app, method=None):
		self.app = app
		app.route = self.route

		if method == None:
			self.method = 'ajax'
		elif isinstance(method, method.__class__) == True:
			self.socketio = method
			self.method = 'socketio'
		else:
			raise TypeError('No valid method was provided')

		self.routes = []



	@staticmethod
	def build_route_pattern(route):
		# gets the name of the variable (surrounded by `< * >`)
		route_regex = re.sub(r'(<\w+>)', r'(?P\1.+)', route)
		# compiles it into a glorious regex
		return re.compile("^{}$".format(route_regex))

	def route(self, rule, no_preload=False, no_ajax_socket_load=False, route_exclude=False, **options):
		def decorator(f):
			@wraps(f)
			def decorated_function(ajax_socket_call=False, *args, **kwargs):
				if route_exclude:
					return f(*args, **kwargs)
				elif ajax_socket_call == False:
					if no_preload:
						return render_template('index.html')
					else:
						return render_template('index.html', preload_content=f(*args, **kwargs))
				else:
					if no_ajax_socket_load:
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
			if self.method == 'socketio':
				# socketio emits the page
				self.socketio.emit('page', base64.b64encode(view_function(ajax_socket_call=True, **kwargs)), namespace='/page')
			elif self.method == 'ajax':
				return base64.b64encode(view_function(ajax_socket_call=True, **kwargs))
		else:
			return 404
