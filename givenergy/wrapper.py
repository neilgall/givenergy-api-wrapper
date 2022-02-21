from flask import Flask, session, abort
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


@app.route('/solarStatus')
def get_plant_summary():
  rsp = client.post(f'{GIVENERGY_BASE_URL}/plant/getPlantSummary')
  if rsp.status_code != 200:
    abort(500)
  return rsp.content
