import pyDes
import base64


def __encrypt(data, key):
    des = pyDes.des(key, pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
    ecryptdata = des.encrypt(data)
    return bytes.decode(base64.b64encode(ecryptdata))  # base64 encoding bytes


def __decrypt(ecryptdata, key):
    des = pyDes.des(key, pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
    data = des.decrypt(base64.b64decode(ecryptdata))  # base64 decoding bytes
    return bytes.decode(data)


if __name__ == '__main__':
    uuid = '03000200-0400-0500-0006-000700080008'
    verification = __encrypt(uuid, '19901012')
    print(verification)
    print(__decrypt(verification, '19901012'))
