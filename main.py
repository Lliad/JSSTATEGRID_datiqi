from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
import pandas as pd
import numpy as np
from typing import Optional
import re
import subprocess
import uuid
import configparser
import pyDes
import base64

writer = pd.ExcelFile(r'.\题库.xlsx')
df = pd.read_excel(writer, dtype={'题干': np.str_})
df = df.applymap(str)
stem = list(df['题干'].values)
df = pd.read_excel(writer, dtype={'答案': np.str_})
df = df.applymap(str)
anwser = list(df['答案'].values)
for i in range(len(stem)):
    stem[i] = stem[i].replace(' ', '')


def anwser_machine(stem, anwser):
    opt = ChromeOptions()
    opt.binary_location = './Chrome/Application/chrome.exe'
    opt.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=Service('./chromedriver.exe'), options=opt)
    driver.maximize_window()
    driver.get(
        'http://ids.js.sgcc.com.cn:8080/nidp/idff/sso?RequestID=idx6hr.S2z5-8QYS.YqeLLYwJpX9s&MajorVersion=1&MinorVersion=2&IssueInstant=2022-08-01T06%3A54%3A40Z&ProviderID=http%3A%2F%2Fuserauth.js.sgcc.com.cn%3A80%2Fnesp%2Fidff%2Fmetadata&RelayState=MA%3D%3D&consent=urn%3Aliberty%3Aconsent%3Aunavailable&ForceAuthn=false&IsPassive=false&NameIDPolicy=onetime&ProtocolProfile=http%3A%2F%2Fprojectliberty.org%2Fprofiles%2Fbrws-art&target=http%3A%2F%2Fuserauth.js.sgcc.com.cn%2FUALogin%2Flogin%3FTRAGEURL%3Dhttp%253A%252F%252Felearning.js.sgcc.com.cn%252Fsso%252Flogin%252F%253FreturnUrl%253Dhttp%25253A%25252F%25252Felearning.js.sgcc.com.cn%25252FthirdIndex&AuthnContextStatementRef=name%2Fpassword%2Furi')
    break_while = False
    while True:
        n = driver.window_handles
        for i in n:
            driver.switch_to.window(i)
            try:
                if driver.find_element(By.XPATH, '/html/head/title').get_attribute('textContent') == '考试详情':
                    break_while = True
                    break
            except:
                continue
        if break_while:
            break
    driver.find_element(By.XPATH, '/html/body/div[4]/div/button[2]').click()
    WebDriverWait(driver, 60).until(EC.visibility_of_element_located(
        (By.XPATH, '/html/body/div[3]/div[3]/div[2]/div/div[1]/div[2]/div[1]/div/div[1]/span[2]')))
    # 单选题
    for i in range(1, 301):
        try:
            subject = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div[2]/div/div[1]/div[2]/div[' + str(
                i) + ']/div/div[1]/span[2]').text
        except:
            break
        subject = subject[0:subject.rfind('（')].replace(' ', '')
        print(subject)
        try:
            anwser_one = anwser[stem.index(subject)]
        except:
            continue
        for ii in range(1, 9):
            try:
                option = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div[2]/div/div[1]/div[2]/div[' + str(
                    i) + ']/div/ul/li[' + str(ii) + ']/input').get_attribute('value')
            except:
                break
            if option in anwser_one:
                print(option)
                driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div[2]/div/div[1]/div[2]/div[' + str(
                    i) + ']/div/ul/li[' + str(ii) + ']/label/i[1]').click()
    # 多选题
    for i in range(1, 301):
        try:
            subject = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div[2]/div/div[2]/div[2]/div[' + str(
                i) + ']/div/div[1]/span[2]').text
        except:
            break
        subject = subject[0:subject.rfind('（')].replace(' ', '')
        print(subject)
        try:
            anwser_one = anwser[stem.index(subject)]
        except:
            continue
        for ii in range(1, 9):
            try:
                option = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div[2]/div/div[2]/div[2]/div[' + str(
                    i) + ']/div/ul/li[' + str(ii) + ']/input').get_attribute('value')
            except:
                break
            if option in anwser_one:
                print(option)
                driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div[2]/div/div[2]/div[2]/div[' + str(
                    i) + ']/div/ul/li[' + str(ii) + ']/label/i[1]').click()
    # 判断题
    for i in range(1, 301):
        try:
            subject = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div[2]/div/div[3]/div[2]/div[' + str(
                i) + ']/div/div[1]/span[2]').text
        except:
            break
        subject = subject[0:subject.rfind('（')].replace(' ', '')
        print(subject)
        try:
            anwser_one = anwser[stem.index(subject)]
        except:
            continue
        for ii in range(1, 9):
            try:
                option = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div[2]/div/div[3]/div[2]/div[' + str(
                    i) + ']/div/ul/li[' + str(ii) + ']/input').get_attribute('value')
            except:
                break
            if option in anwser_one:
                print(option)
                driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div[2]/div/div[3]/div[2]/div[' + str(
                    i) + ']/div/ul/li[' + str(ii) + ']/label/i[1]').click()
    driver.quit()


def get_windows_uuid() -> Optional[uuid.UUID]:
    try:
        # Ask Windows for the device's permanent UUID. Throws if command missing/fails.
        txt = subprocess.check_output("wmic csproduct get uuid").decode()

        # Attempt to extract the UUID from the command's result.
        match = re.search(r"\bUUID\b[\s\r\n]+([^\s\r\n]+)", txt)
        if match is not None:
            txt = match.group(1)
            if txt is not None:
                # Remove the surrounding whitespace (newlines, space, etc)
                # and useless dashes etc, by only keeping hex (0-9 A-F) chars.
                txt = re.sub(r"[^0-9A-Fa-f]+", "", txt)

                # Ensure we have exactly 32 characters (16 bytes).
                if len(txt) == 32:
                    return uuid.UUID(txt)
    except:
        pass  # Silence subprocess exception.

    return None


def readverification():
    config = configparser.ConfigParser()
    config.read('./verification.ini', encoding='utf-8')
    vf = config.get('verification', 'uuid')
    return vf


def writeverification(vf):
    config = configparser.ConfigParser()
    config.add_section('verification')
    config.set('verification', 'uuid', vf)
    config.write(open('./verification.ini', 'w'))


def __encrypt(data, key):
    des = pyDes.des(key, pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
    ecryptdata = des.encrypt(data)
    return bytes.decode(base64.b64encode(ecryptdata))  # base64 encoding bytes


def __decrypt(ecryptdata, key):
    des = pyDes.des(key, pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
    data = des.decrypt(base64.b64decode(ecryptdata))  # base64 decoding bytes
    return bytes.decode(data)


while True:
    try:
        vf = str(__decrypt(readverification(), '19901012'))
    except:
        print('验证失败！')
        print('本机机器码：' + str(get_windows_uuid()))
        yzm = input('请输入验证码：')
        writeverification(yzm)
        continue
    if vf == str(get_windows_uuid()):
        print('验证通过！')
        break
    else:
        print('验证失败！')
        print('本机机器码：' + str(get_windows_uuid()))
        yzm = input('请输入验证码：')
        writeverification(yzm)
anwser_machine(stem, anwser)
