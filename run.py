#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from flask import Flask, redirect, url_for, request
from flask import jsonify, abort
import sys
import logging
import paho.mqtt.client as mqtt
app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

def on_connect(client, userdata, flags, rc):
    app.logger.error("Connected with result code "+str(rc))

def on_publish(client, userdata, mid):
    app.logger.error('on_publish: %s', str(mid))

def on_disconnect(client, userdata, rc):
    app.logger.error('on_disconnect: %s', str(rc))

client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish
client.on_disconnect = on_disconnect
client.connect_async("storybox.athenamuses.cn", 1884, 60)
client.loop_start()

def log(*args):
  print(args[0] % (len(args) > 1 and args[1:] or []))
  sys.stdout.flush()

@app.route('/hello/')
def hello_world():
	return 'Hello world'

@app.route('/success/<name>')
def success(name):
	return 'welcome %s' % name

@app.route('/login', methods = ['POST', 'GET'])
def login():
	if request.method == "POST":
		user = request.form['nm']
		return redirect(url_for('success', name = user))
	else:
		user = request.args.get('nm')
		return redirect(url_for('success', name = user))

@app.route('/' , methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
      if not request.json:
         abort(400)
      a = request.get_data()
      dict1 = json.loads(a)
      #log('recv: %s' % a)
      app.logger.error('recv: %s', a)
      client.publish("xiaobaoaudio", "play", 1)

      return redirect(url_for('hello_world'))#json.dumps(dict1["data"])
  else:
      return '<h1>只接受post请求！</h1>'

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=8080, debug=True)
