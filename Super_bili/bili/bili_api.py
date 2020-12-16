import requests

from time import time
from bili.rsa_bili import Rsa_a, Getkey

key = Getkey()
access_key = key.login()


async def pc_pgc_pcurl(params):
    from bili.model.pc_pgc_pcurl import url, headers, data

    appkey = params.get("appkey", "84956560bc028eb7")
    cid = params.get("cid", "")
    fnval = params.get("fnval", "")
    fourk = params.get("fourk", "")
    qn = params.get("qn", "64")
    data["access_key"] = access_key
    data["appkey"] = appkey
    data["cid"] = cid
    data["fnval"] = fnval
    data["fourk"] = fourk
    data["qn"] = qn
    data["ts"] = int(time())
    md5 = Rsa_a()
    sign_params = md5.sign(data)
    req = requests.get(url + sign_params, headers=headers, timeout=5)
    return req.text
