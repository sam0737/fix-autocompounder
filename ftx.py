import time
import hmac
import json
from config import *

from urllib.request import Request, urlopen, HTTPError, URLError, HTTPErrorProcessor, build_opener

class XH(HTTPErrorProcessor):
    def http_response(self, request, response):
        return response
    https_response = http_response

def call_ftx(method, path, payload=None):
    path = path.lstrip('/')
    payload_json = ''
    if payload is not None:
        payload_json = json.dumps(payload)

    request = Request(f'https://ftx.com/api/{path}', method=method, data=payload_json.encode())

    ts = int(time.time() * 1000)
    signature_payload = f'{ts}{method}/api/{path}{payload_json}'.encode()
    # print(signature_payload)
    signature = hmac.new(API_SECRET.encode(), signature_payload, 'sha256').hexdigest()

    request.add_header('FTX-KEY', API_KEY)
    request.add_header('FTX-SIGN', signature)
    request.add_header('FTX-TS', str(ts))
    request.add_header('Content-type', 'application/json')
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36')

    try:
        opener = build_opener() # build_opener(XH)
        with opener.open(request, timeout=10) as response:
            r = response.read()
            # print(r)
            return json.loads(r)
    except HTTPError as e:
        raise


