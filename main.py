#!/usr/bin/env python

from app import app, singleview, socketio

if __name__ == "__main__":
	socketio.run(app, port=5000, debug=True)