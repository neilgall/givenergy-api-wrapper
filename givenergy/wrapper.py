from flask import Flask, request, session, abort
import datetime
import json
import os
import requests
import secrets


GIVENERGY_BASE_URL = 'https://api.givenergy.cloud/v1'
API_TOKEN = os.environ['API_TOKEN']

app = Flask(__name__)
app.secret_key = secrets.token_bytes(16)

client = requests.Session()
client.headers.update({
  'Accept': 'application/json',
  'Content-Type': 'application/json',
  'Authorization': f'Bearer {API_TOKEN}'
})

device_info = client.get(f'{GIVENERGY_BASE_URL}/communication-device').json()
print(device_info)
inverter = device_info['data'][0]['inverter']['serial']


@app.route('/solar/current')
def get_current_data():
  return client.get(f'{GIVENERGY_BASE_URL}/inverter/{inverter}/system-data/latest').content


@app.route('/solar/date')
def get_daily_data():
  year = int(request.args['year'])
  month = int(request.args['month'])
  day = int(request.args['day'])

  rsp = post(f'/plantChart/monthColumn?plantId={PLANT_ID}&year={year}&month={month}')
  return next(item for item in rsp['data'] if item['day'] == day)
