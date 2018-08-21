# -*- coding: utf-8 -*-

__author__ = 'ufian'

import contextlib
import os
import sh
import threading
import yaml
import requests
from flask import Flask, abort, request


app = Flask(__name__)

config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'notify.yaml')
try:
    config = {}
    with open(config_path) as f:
        config = yaml.load(f.read())
except:
    pass

def send_message(configchat, text):
    api_url = 'https://api.telegram.org/bot{}'.format(configchat['token'])
    name = 'sendMessage'
    
    params = {
        'text': text,
        'chat_id': configchat['user']
    }
    
    res = requests.request(
        'POST',
        api_url + '/{0}'.format(name),
        params=params,
        timeout=30
    )

def send(channel, message):
    if channel in config:
        send_message(config[channel], message)


@contextlib.contextmanager
def cd(path):
   old_path = os.getcwd()
   os.chdir(path)
   try:
       yield
   finally:
       os.chdir(old_path)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/notify', methods=['GET', 'POST'])
def notify():
    channel = request.args.get('channel')
    text = request.args.get('text')
    
    if channel and text:
        send(channel, text)

    return "Ok"

@app.route('/deploy/<service>', methods=['GET', 'POST'])
def deploy(service):
    if service not in {'twitory', 'udmurt', 'ccal', 'tatarin', 'awdinfo'}:
        abort(404)
        return
    
    with cd('/root/{0}'.format(service)):
        sh.git("pull")
        sh.docker_compose("restart")

    return "Ok"


@app.route('/stop/<service>', methods=['GET', 'POST'])
def stop(service):
    if service not in {'udmurt'}:
        abort(404)
        return
    
    with cd('/root/{0}'.format(service)):
        sh.docker_compose("stop")

    return "Ok"
    
@app.route('/start/<service>', methods=['GET', 'POST'])
def start(service):
    if service not in {'udmurt'}:
        abort(404)
        return
    
    with cd('/root/{0}'.format(service)):
        sh.git("pull")
        sh.docker_compose("start")

    return "Ok"
