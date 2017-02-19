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
singleview = singleview(app, socketio)

# socketio
#######################################################

@socketio.on('get page', namespace='/page')
def socket_page(data):
	singleview.serve(data['page'])

# routes
#######################################################

@app.route('/', no_preload=True, no_socket_load=True)
def index():
	template_vars = {}
	return render_template('index.html', **template_vars)

@app.route('/<path:path>')
def static_proxy(path):
	return app.send_static_file(path)

#######################################################

@app.route('/1')
def route_1():
	values = {"data": "page 1"}
	return render_template('default.html', **values)

@app.route('/2')
def route_2():
	values = {"data": "page 2"}
	return render_template('default.html', **values)

@app.route('/3')
def route_3():
	values = {"data": "page 3"}
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