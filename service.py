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
    if service not in {'twitory', 'udmurt'}:
        abort(404)
        return
    
    with cd('/root/{0}'.format(service)):
        sh.git("pull")
        sh.docker_compose("restart")

    # def after_request():
    #     with cd('/root/nginx'):
    #         sh.docker_compose("restart")
    #
    # threading.Timer(1, after_request).start()
    return "Ok"
