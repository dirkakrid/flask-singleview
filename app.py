#!/usr/bin/env python
from flask import Flask, render_template, redirect, url_for, request, session, send_from_directory, jsonify
from flask_socketio import SocketIO
import requests, json, base64, sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask_singleview import singleview

# flask setup
app = Flask(__name__)
app.threaded = True
app.debug = True
app.secret_key = 'secret'

socketio = SocketIO(app)
singleview = singleview(app)

# socketio
#######################################################

@socketio.on('get page', namespace='/page')
def socket_page(data):
	singleview.serve(data['page'])

@app.route('/page', route_exclude=True, methods=['POST'])
def singleview_ajax_page():
	print request.referrer
	if request.method == 'POST':
		return singleview.serve(request.form['page'])

# routes
#######################################################

@app.route('/', no_preload=True, no_ajax_socket_load=True, methods=['GET'])
def index():
	template_vars = {}
	return render_template('index.html', **template_vars)

@app.route('/<path:path>')
def static_proxy(path):
	return app.send_static_file(path)

#######################################################

@app.route('/1')
def route_1():
	values = {"data": "this is page 1<br><a href='##2'>page 2</a>"}
	return render_template('default.html', **values)

@app.route('/2')
def route_2():
	values = {"data": "this is page 2<br><a href='##3/pipskweak'>page 3</a>"}
	return render_template('default.html', **values)

@app.route('/3/<name>')
def route_3(name=None):
	values = {"data": "this is page 3<br><a href='##1'>page 1</a> {}".format(name)}
	return render_template('default.html', **values)

# errors
#######################################################

# 404 error; not found
@app.errorhandler(404)
def err_404(e):
	return '404', 404

# 500 error; server error
@app.errorhandler(500)
def err_500(e):
	return '500', 500

#######################################################

if __name__ == "__main__":
	socketio.run(app, port=5000, debug=True)
