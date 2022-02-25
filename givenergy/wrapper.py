from flask import Flask, request, session, abort
import datetime
import json
import os
import requests
import secrets


GIVENERGY_BASE_URL = 'https://www.givenergy.cloud/GivManage/api'
USERNAME = os.environ['USERNAME']
PASSWORD = os.environ['PASSWORD']

app = Flask(__name__)
app.secret_key = secrets.token_bytes(16)

client = requests.Session()
client.headers.update({'Accept': 'application/json'})

def login():
  client.post(f'{GIVENERGY_BASE_URL}/login?account={USERNAME}&password={PASSWORD}')
  plants = client.post(f'{GIVENERGY_BASE_URL}/plant/getPlantList').json()  
  PLANT_ID = plants['rows'][0]['plantId']

def post(path):
  def do_post(path):
    rsp = client.post(f'{GIVENERGY_BASE_URL}{path}')
    if rsp.status_code != 200:
      abort(500)
    return rsp.json()

  rsp_json = do_post(path)
  if not rsp_json.get('success'):
    login()
    rsp_json = do_post(path)
  return rsp_json


@app.route('/solar/current')
def get_plant_summary():
  return json.dumps(post('/plant/getPlantSummary'))


@app.route('/solar/date')
def get_daily_data():
  year = int(request.args['year'])
  month = int(request.args['month'])
  day = int(request.args['day'])

  rsp = post(f'/plantChart/monthColumn?plantId={PLANT_ID}&year={year}&month={month}')
  return next(item for item in rsp['data'] if item['day'] == day)
