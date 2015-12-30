import requests
import binascii

def send(ct):
    url = "http://localhost:4242/api"
    data = {
        'c': binascii.hexlify(ct)
    }
    r = requests.get(url, params=data)
    return r.status_code == 200

data = binascii.unhexlify(raw_input())

print send(data)
