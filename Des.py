import pyDes
import base64
import time
import requests


def __encrypt(data, key):
    des = pyDes.des(key, pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
    ecryptdata = des.encrypt(data)
    return bytes.decode(base64.b64encode(ecryptdata))  # base64 encoding bytes


def __decrypt(ecryptdata, key):
    des = pyDes.des(key, pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
    data = des.decrypt(base64.b64decode(ecryptdata))  # base64 decoding bytes
    return bytes.decode(data)

def trans_format(time_string, from_format, to_format='%Y.%m.%d %H:%M:%S'):
    """
    @note 时间格式转化
    :param time_string:
    :param from_format:
    :param to_format:
    :return:
    """
    time_struct = time.strptime(time_string,from_format)
    times = time.strftime(to_format, time_struct)
    return times


if __name__ == '__main__':
    uuid = 'e53fdc50-9ac7-11e5-9310-f18c20b51800'
    days = '30'
    web_date = requests.get('http://elearning.js.sgcc.com.cn/index').headers['Date']
    format_web_date = trans_format(web_date, '%a, %d %b %Y %H:%M:%S GMT', '%Y-%m-%d')
    verification = __encrypt(uuid + '&' + format_web_date + '&' + days, '19901012')
    print(verification)
    print(__decrypt(verification, '19901012'))
