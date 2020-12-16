import base64
import rsa
import requests
import hashlib
import ujson
from time import time
from urllib import parse

# pipreqs . --encoding=utf8 --force


class Rsa_a(object):
    def __init__(self):
        self.username = ""  # 大会员账号
        self.password = ""  # 大会员密码
        ###
        self.pc_APPKEY = "84956560bc028eb7"
        self.pc_SECRET = "94aba54af9065f71de72f5508f1cd42e"
        ###
        self.android_APPKEY = "1d8b6e7d45233436"
        self.android_SECRET = "560c52ccd288fed045859ed18bffd973"

    def sign(self, params):
        data = ""
        secret = ""
        appkey = params.setdefault(("appkey"), "84956560bc028eb7")
        if params.setdefault(("sign"), None) != None:
            del params["sign"]
        else:
            del params["sign"]
        if appkey == "1d8b6e7d45233436":
            secret = self.android_SECRET
        else:
            secret == self.pc_SECRET
        paras = sorted(params)
        paras.sort()
        for para in paras:
            if data != "":
                data += "&"
            data += para + "=" + str(params[para])
        m = hashlib.md5()
        m.update((data + secret).encode("utf-8"))
        return data + "&sign=" + m.hexdigest()

    def rsa_pass(self, password, pub_key, hash):
        pub_key = rsa.PublicKey.load_pkcs1_openssl_pem(pub_key.encode("utf-8"))
        pass_rsa = parse.quote_plus(
            base64.b64encode(rsa.encrypt(f"{hash}{password}".encode(), pub_key))
        )
        return pass_rsa


class Getkey(Rsa_a):
    def __init__(self):
        super().__init__()
        self.getrsa_url = "https://passport.bilibili.com/api/oauth2/getKey"
        self.login_url = "https://passport.bilibili.com/api/v3/oauth2/login"
        self.headers = {
            "Host": "passport.bilibili.com",
            "APP-KEY": "android",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "BiliDroid/6.8.0 os/android",
        }
        self.time = int(time())

    def get(self):
        params = {
            "actionKey": "appkey",
            "appkey": self.android_APPKEY,
            "build": "6080500",
            "device": "android",
            "mobi_app": "android",
            "platform": "android",
            "ts": self.time,
        }
        sign_params = self.sign(params)
        a = requests.post(
            self.getrsa_url, data=sign_params, headers=self.headers, timeout=5
        )
        return a.text

    def login(self):
        try:
            login_rsa = ujson.loads(self.get())
            login_hash = login_rsa["data"]["hash"]
            login_rsa_key = login_rsa["data"]["key"]
            self.password_rsa = self.rsa_pass(self.password, login_rsa_key, login_hash)
            params = {
                "actionKey": "appkey",
                "appkey": self.android_APPKEY,
                "appver": "6080500",
                "build": "6080500",
                "captcha": "",
                "challenge": "",
                "device": "android",
                "mobi_app": "android",
                "password": self.password_rsa,
                "permission": "ALL",
                "platform": "android",
                "seccode": "",
                "subid": 1,
                "ts": self.time,
                "username": self.username,
                "validate": "",
            }
            sign_params = self.sign(params)
            res = requests.post(
                self.login_url, data=sign_params, headers=self.headers, timeout=5
            )
            access_key = ujson.loads(res.text)
            return access_key["data"]["token_info"]["access_token"]

        except BaseException as err:
            print(err)
            return "登录错误，错误为:" + str(err)