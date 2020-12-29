import os
import json
import base64
import win32crypt
import sqlite3
from Crypto.Cipher import AES


def decryptcookies(data):
    path = r'%LocalAppData%\Google\Chrome\User Data\Local State'
    path = os.path.expandvars(path)
    with open(path, 'r') as file:
        encrypted_key = json.loads(file.read())['os_crypt']['encrypted_key']
    encrypted_key = base64.b64decode(encrypted_key)  # Base64 decoding
    encrypted_key = encrypted_key[5:]  # Remove DPAPI
    decrypted_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    nonce = data[3:3+12]
    ciphertext = data[3+12: -16]
    tag = data[-16:]
    cipher = AES.new(decrypted_key, AES.MODE_GCM, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)  # the decrypted cookie
    return plaintext.decode(encoding='utf-8')


def getcookiesfromchrome(host):
    cookiepath = os.environ['LOCALAPPDATA'] + r'\Google\Chrome\User Data\Default\Cookies'
    sql = r"select name,encrypted_value from cookies where host_key in ('.easy.lagou.com', '.lagou.com', 'easy.lagou.com', '.passport.lagou.com');"
    with sqlite3.connect(cookiepath) as conn:
        cur = conn.cursor()
        cur.execute(sql)
        cookies = {key: decryptcookies(value) for key, value in cur.fetchall()}
        cur.close()
    return cookies




