#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Crypto.Cipher import AES
from base64 import b64decode, b64encode, urlsafe_b64decode, urlsafe_b64encode
import urllib
import hmac, hashlib, base64

padding = '\0'

BS = AES.block_size
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[0:-ord(s[-1])]


def hmac_sha256(key, text):
    message = bytes(text).encode('utf-8')
    secret = bytes(key).encode('utf-8')
    return base64.b64encode(hmac.new(secret, message, digestmod=hashlib.sha256).digest())


def aes_encrypt(key, text):
    mode = AES.MODE_CBC
    cryptor = AES.new(key, mode, b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x00\x01\x02\x03\x04\x05\x06')

    text = str(text)
    ciphertext = cryptor.encrypt(pad(text))
    return ciphertext


def aes_decrypt(key, text):
    mode = AES.MODE_CBC
    cryptor = AES.new(key, mode, b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x00\x01\x02\x03\x04\x05\x06')

    text = str(text)
    plain_text = cryptor.decrypt(text)
    return unpad(plain_text)


def url_encode(text):
    return urllib.urlencode({'c': text})[2:]


def url_decode(text):
    return urllib.unquote(text).decode('utf-8', 'replace').encode('gbk', 'replace')


def encrypt_imeigoo(text, key=None):
    if key == None:
        key = "imeigooooooooooo"

    encrpt_data = aes_encrypt(key, text)
    encrpt_data = b64encode(encrpt_data)
    encrpt_data = url_encode(encrpt_data)
    return encrpt_data


def decrypt_imeigoo(text, key=None):
    if key == None:
        key = "imeigooooooooooo"

    decrypt_data = url_decode(text)
    decrypt_data = b64decode(decrypt_data)
    decrypt_data = aes_decrypt(key, decrypt_data)
    return decrypt_data


##############
# XXTea Begin
##############
import struct

_DELTA = 0x9E3779B9


def _long2str(v, w):
    n = (len(v) - 1) << 2
    if w:
        m = v[-1]
        if (m < n - 3) or (m > n): return ''
        n = m
    s = struct.pack('<%iL' % len(v), *v)
    return s[0:n] if w else s


def _str2long(s, w):
    n = len(s)
    m = (4 - (n & 3) & 3) + n
    s = s.ljust(m, "\0")
    v = list(struct.unpack('<%iL' % (m >> 2), s))
    if w: v.append(n)
    return v


def xxtea_encrypt(text, key):
    if text == '': return text
    v = _str2long(text, True)
    k = _str2long(key.ljust(16, "\0"), False)
    n = len(v) - 1
    z = v[n]
    y = v[0]
    sum = 0
    q = 6 + 52 // (n + 1)
    while q > 0:
        sum = (sum + _DELTA) & 0xffffffff
        e = sum >> 2 & 3
        for p in xrange(n):
            y = v[p + 1]
            v[p] = (v[p] + ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4) ^ (sum ^ y) + (k[p & 3 ^ e] ^ z))) & 0xffffffff
            z = v[p]
        y = v[0]
        v[n] = (v[n] + ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4) ^ (sum ^ y) + (k[n & 3 ^ e] ^ z))) & 0xffffffff
        z = v[n]
        q -= 1
    return _long2str(v, False)


def xxtea_decrypt(text, key):
    if text == '': return text
    v = _str2long(text, False)
    k = _str2long(key.ljust(16, "\0"), False)
    n = len(v) - 1
    z = v[n]
    y = v[0]
    q = 6 + 52 // (n + 1)
    sum = (q * _DELTA) & 0xffffffff
    while (sum != 0):
        e = sum >> 2 & 3
        for p in xrange(n, 0, -1):
            z = v[p - 1]
            v[p] = (v[p] - ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4) ^ (sum ^ y) + (k[p & 3 ^ e] ^ z))) & 0xffffffff
            y = v[p]
        z = v[n]
        v[0] = (v[0] - ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4) ^ (sum ^ y) + (k[0 & 3 ^ e] ^ z))) & 0xffffffff
        y = v[0]
        sum = (sum - _DELTA) & 0xffffffff
    return _long2str(v, True)


##################
# XXTea End
##################

def xx_b64decode(text):
    try:
        return b64decode(text)
    except Exception, e:
        print("xx_b64decode error msg=[%s]" % repr(e))
        return ""


def xx_b64encode(text):
    try:
        return b64encode(text)
    except Exception, e:
        print("xx_b64encode error msg=[%s]" % repr(e))
        return ""


def xx_url_b64decode(text):
    try:
        return urlsafe_b64decode(text + '=' * (4 - len(text) % 4))
    except Exception, e:
        print("xx_url_b64decode error msg=[%s]" % repr(e))
        return ""


def xx_url_b64encode(text):
    try:
        return urlsafe_b64encode(text).rstrip('=')
    except Exception, e:
        print("xx_url_b64encode error msg=[%s]" % repr(e))
        return ""


def xxtea_encrypt_imeigoo(text, key=None):
    if key == None:
        key = "MDk4Nl9mNzkxMm"

    text = text.encode("utf-8")
    return xx_url_b64encode(xxtea_encrypt(text, key))


def xxtea_decrypt_imeigoo(text, key=None):
    if key == None:
        key = "MDk4Nl9mNzkxMm"

    text = text.encode("utf-8")
    return xxtea_decrypt(xx_url_b64decode(text), key)


##################
# 简单算法
##################
def simple_encrypt(key, s):
    key = len(key)

    b = bytearray(str(s).encode("gbk"))
    n = len(b)  # 求出 b 的字节数
    c = bytearray(n * 2)
    j = 0
    for i in range(0, n):
        b1 = b[i]
        b2 = b1 ^ key  # b1 = b2^ key
        c1 = b2 % 16
        c2 = b2 // 16  # b2 = c2*16 + c1
        c1 = c1 + 65
        c2 = c2 + 65  # c1,c2都是0~15之间的数,加上65就变成了A-P 的字符的编码
        c[j] = c1
        c[j + 1] = c2
        j = j + 2
    return c.decode("gbk")


def simple_decrypt(key, s):
    key = len(key)

    c = bytearray(str(s).encode("gbk"))
    n = len(c)  # 计算 b 的字节数
    if n % 2 != 0:
        return ""
    n = n // 2
    b = bytearray(n)
    j = 0
    for i in range(0, n):
        c1 = c[j]
        c2 = c[j + 1]
        j = j + 2
        c1 = c1 - 65
        c2 = c2 - 65
        b2 = c2 * 16 + c1
        b1 = b2 ^ key
        b[i] = b1
    try:
        return b.decode("gbk")
    except:
        return "failed"