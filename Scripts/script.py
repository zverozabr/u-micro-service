from services.Utils import getAbsoluteRelative
from requests import Session
import subprocess
import shutil
import csv
import os
# import time


def getCsvAsList(path):

    with open(path, newline='') as csvfile:
        data = list(csv.reader(csvfile))
    return data


def rmDir(path):
    shutil.rmtree(os.path.dirname(path))


def getIm(im, token):
    url = 'http://'+os.getenv('SERVER_NAME') + '/v1/'
    part = f'images/{im}?format=TIF&download=True'
    url = url + part
    session = Session()
    session.headers.update({'Authorization': f'Bearer {token}'})
    responce = session.get(url)

    print(responce)
    if responce.status_code == 200:
        data = responce.json()
        if data is not None and len(data) > 0:
            data = data['data'][0]
            if len(data['paths']) > 0:
                path = data['paths'][0]
                realpath = (getAbsoluteRelative(path['path'], True))
                if os.path.exists(realpath):
                    return realpath
    return None


def postRes(token, data):
    url = 'http://'+os.getenv('SERVER_NAME') + '/v1/'
    part = 'resource'
    url = url + part
    session = Session()
    session.headers.update({'Authorization': f'Bearer {token}'})
    responce = session.post(url, json=data)
    if responce.status_code == 200:
        data = responce.json()
        return data
    return None


def startProcessSegm(path, script, size=20):
    csvName = os.path.splitext(os.path.basename(path))[0] + '.csv'
    csvName = f'{os.path.dirname(path)}/{csvName}'
    arrToStart = (['pipenv', 'run', 'python',  script, os.path.abspath(path), '--bounds', '0:', '0:', '--size', str(size), '--debug', 'False', '-o', csvName, '-c', '0'])
    finish = subprocess.Popen(arrToStart, shell=False, stdout=True)
    finish.wait()
    return csvName


def run():
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYyMjcxMzUxNCwianRpIjoiZDM2ZWFlNTMtMDQwYS00OTJiLTliZDUtOTQ0NWUwYWZjMGYzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJsb2dpbiI6InJvb3QiLCJpZCI6IjIwMTM4MiJ9LCJuYmYiOjE2MjI3MTM1MTQsImV4cCI6MTYyMzMxODMxNH0.3ZyRYhETKcCQUEw-nGdDfe50dcZs7Ks5NBT4Xn4xvpE'
    scriptpath = '//DATA_STORAGE/Scripts/Segmentation.py'
    im = 1
    realpath = getIm(im, token)
    if realpath is not None:
        csv_path = startProcessSegm(path=realpath, script=scriptpath, size=20)
        if csv_path is not None:
            # time.sleep(1200)
            data = getCsvAsList(csv_path)
            back_js = {
                'name': 'segmentation',
                'content': 'unversal microservice',
                'omeroId': im,
                'omeroIds': [im],
                'ids': [],
                'tasks': [
                    {
                        'csvdata': data,
                        'name': 'segmentation',
                        'content': 'unversal microservice',
                        'omeroId': im,
                        'status': 100
                    }
                ]
            }

            postRes(token, back_js)
            print(back_js)
    else:
        print('cannot download from url')

    # time.sleep(1200)
    print('success')
