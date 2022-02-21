from flask import Flask, request, session, abort
import datetime
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
client.post(f'{GIVENERGY_BASE_URL}/login?account={USERNAME}&password={PASSWORD}')

plants = client.post(f'{GIVENERGY_BASE_URL}/plant/getPlantList').json()
PLANT_ID = plants['rows'][0]['plantId']


@app.route('/solar/current')
def get_plant_summary():
  rsp = client.post(f'{GIVENERGY_BASE_URL}/plant/getPlantSummary')
  if rsp.status_code != 200:
    abort(500)
  return rsp.content


@app.route('/solar/date')
def get_daily_data():
  year = int(request.args['year'])
  month = int(request.args['month'])
  day = int(request.args['day'])

  rsp = client.post(f'{GIVENERGY_BASE_URL}/plantChart/monthColumn?plantId={PLANT_ID}&year={year}&month={month}')
  if rsp.status_code != 200:
    abort(500)
  return next(item for item in rsp.json()['data'] if item['day'] == day)
