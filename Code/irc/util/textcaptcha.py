#!/usr/bin/python3

import hashlib
import json
import requests

url = "http://api.textcaptcha.com/krowbar@tilde.town.json"

def get_captcha():
  return json.loads(requests.get(url).content.decode())

