import binascii
import base64
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from flask import Flask, request, abort, render_template

app = Flask(__name__)

KEY = os.urandom(16)
IV = os.urandom(16)
SECRET = base64.b64decode("T2RlIHRvIEVDQgpieSBCZW4gTmFneSAtIFBPQ3x8R1RGTyAweDA0CgpPaCBsaXR0bGUgb25lLCB5b3XigJlyZSBncm93aW5nIHVwCllvdeKAmWxsIHNvb24gYmUgd3JpdGluZyBDCllvdeKAmWxsIHRyZWF0IHlvdXIgaW50cyBhcyBwb2ludGVycwpZb3XigJlsbCBuZXN0IHRoZSB0ZXJuYXJ5CllvdeKAmWxsIGN1dCBhbmQgcGFzdGUgZnJvbSBnaXRodWIKQW5kIHRyeSBjcnlwdG9ncmFwaHkKQnV0IGV2ZW4gaW4geW91ciBkYXJrZXN0IGhvdXIKRG8gbm90IHVzZSBFQ0IKQ0JD4oCZcyBCRUFTVGx5IHdoZW4gcGFkZGluZ+KAmXMgYWJ1c2VkCkFuZCBDVFLigJlzIGZpbmUgdGlsIGEgbm9uY2UgaXMgcmV1c2VkClNvbWUgc2F5IGl04oCZcyBhIENSSU1FIHRvIGNvbXByZXNzIHRoZW4gZW5jcnlwdApPciBzdG9yZSBrZXlzIGluIHRoZSBicm93c2VyIChvciB1c2UgamF2YXNjcmlwdCkKRGlmZmllIEhlbGxtYW4gd2lsbCBjb2xsYXBzZSBpZiBoYWNrZXJzIGNob29zZSB5b3VyIGcKQW5kIFJTQSBpcyBmdWxsIG9mIHRyYXBzIHdoZW4gZSBpcyBzZXQgdG8gMwpXaGl0ZW4hIEJsaW5kISBJbiBjb25zdGFudCB0aW1lISBEb27igJl0IHdyaXRlIGFuIFJORyEKQnV0IGZhaWxpbmcgYWxsLCBhbmQgbGlzdGVuIHdlbGw6IERvIG5vdCB1c2UgRUNCClRoZXnigJlsbCBzYXkg4oCcSXTigJlzIGxpa2UgYSBvbmUtdGltZS1wYWQhClRoZSBkYXRh4oCZcyBzaG9ydCwgaXTigJlzIG5vdCBzbyBiYWQKdGhlIGtleXMgYXJlIGxvbmfigJR0aGV54oCZcmUgaXJvbiBjbGFkCkkgaGF2ZSBhIFBoRCHigJ0KQW5kIHRoZW4geW914oCZcmUgZnJvbnQgcGFnZSBIYWNrZXIgTmV3cwpZb3VyIHBhc3N3b3JkcyBjcmFja2Vk4oCUQWRvYmUgQmx1ZXMuCkRvbuKAmXQgbGVhdmUgeW91ciBwZW5ndWluIHNob3dpbmcgdGhyb3VnaCwKRG8gbm90IHVzZSBFQ0I=")  # Don't spoiler yourself!
cipher = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
encryptor = cipher.encryptor()
padder = padding.PKCS7(128).padder()
plaintext = padder.update(SECRET) + padder.finalize()
MSG = IV + encryptor.update(plaintext) + encryptor.finalize()

@app.route('/')
def show_info():
    return render_template('info.html', ciphertext=binascii.hexlify(MSG))

@app.route('/api')
def handle_api():
    if not 'c' in request.args: abort(400)

    ct = binascii.unhexlify(request.args['c'])
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ct) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    message = unpadder.update(plaintext) + unpadder.finalize()

    return 'Thanks!'


if __name__ == '__main__':
    app.run(port=4242)
