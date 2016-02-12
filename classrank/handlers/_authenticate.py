try:
    import scrypt as scrypt

    debug = False
except ImportError:
    import pyscrypt as scrypt

    debug = True

import uuid

N = 2 ** 14
p = 1
r = 8
buflen = 128


def hash_pw(password, salt):
    if type(password) != bytes:
        password = bytes(password, 'utf-8')

    if debug:
        h = scrypt.hash(password, salt, N=2 ** 4, p=1, r=1, dkLen=buflen)
    else:
        h = scrypt.hash(password, salt, N=N, p=p, r=r, buflen=buflen)

    return h


def create_password(password):
    if type(password) != bytes:
        password = bytes(password, 'utf-8')

    salt = uuid.uuid4().bytes
    return hash_pw(password, salt), salt
