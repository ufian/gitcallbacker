# -*- coding: utf-8 -*-

__author__ = 'ufian'

import contextlib
import os
import sh
from flask import Flask
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

@app.route('/deploy')
def deploy():
    with cd('/root/twitory'):
        sh.git("pull")
        sh.docker_compose("restart")

    with cd('/root/nginx'):
        sh.docker_compose("restart")
