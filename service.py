# -*- coding: utf-8 -*-

__author__ = 'ufian'

import contextlib
import os
import sh
import threading
from flask import Flask, abort
app = Flask(__name__)



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

@app.route('/deploy/<service>', methods=['GET', 'POST'])
def deploy(service):
    if service not in {'twitory', 'udmurt', 'ccal'}:
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
