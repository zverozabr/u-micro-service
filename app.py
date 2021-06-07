from config import config, fromFile
from flask import Flask
from flask_cors import CORS
import os
import sys
from pipfile import Pipfile
import subprocess
import importlib
import shutil

application = Flask(__name__)
application.config.from_mapping(config)
CORS(application, supports_credentials=True)


def installPacks(path):
    parsed = Pipfile.load(filename=os.path.dirname(path) + '/Pipfile')
    current = Pipfile.load(filename='Pipfile')
    arrToInstall = []
    for key in parsed.data['default']:
        lib_in_current_project = current.data['default'].get(key)
        lib_in_script_project = parsed.data['default'].get(key)
        if lib_in_current_project != lib_in_script_project:
            if lib_in_script_project == "*":
                lib_in_script_project = ''
            lib_in_script_project = lib_in_script_project.replace('=', '')
            if lib_in_script_project != '':
                lib_in_script_project = '==' + lib_in_script_project
            arrToInstall.append(key+lib_in_script_project)
    if len(arrToInstall) > 0:
        for lib in arrToInstall:

            arrToStart = (['pipenv', 'install', lib])
            finish = subprocess.Popen(arrToStart, shell=False, stdout=True)
            finish.wait()


def unistallPacks():
    current = Pipfile.load(filename='Pipfile')
    template = Pipfile.load(filename='Pipfile_template')
    arrToRemove = []
    for key in current.data['default']:
        lib_in_current_project = current.data['default'].get(key)
        lib_in_template = template.data['default'].get(key)
        if lib_in_current_project != lib_in_template:
            arrToRemove.append(key)
    for lib in arrToRemove:
        arrToStart = ['pipenv', 'uninstall', lib]
        finish = subprocess.Popen(arrToStart, shell=False, stdout=True)
        finish.wait()
    return arrToRemove


if __name__ == '__main__':
    path = os.getenv("SCRIPT_PATH")
    if path is not None:
        if os.path.exists(path):
            sys.path.insert(0, os.path.dirname(path))
            if os.path.exists(os.path.dirname(path) + '/Pipfile'):
                installPacks(path)
            else:
                arrToRemove = unistallPacks()
                if len(arrToRemove) > 0:
                    if os.path.exists('Pipfile'):
                        os.remove('Pipfile')
                    if os.path.exists('Pipfile.lock'):
                        os.remove('Pipfile.lock')
                    shutil.copyfile('Pipfile_template', 'Pipfile')
                    shutil.copyfile('Pipfile_template.lock', 'Pipfile.lock')

            if os.path.exists(os.path.dirname(path) + '/.env.script'):
                application.config.from_mapping(fromFile(os.path.dirname(path) + '/.env.script'))

            script = importlib.import_module('script')
            script.run()
        else:
            print('path problem')
