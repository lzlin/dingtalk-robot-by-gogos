# -*- coding:utf-8 –*-
from flask import Flask,request,redirect
import dingtalk
from ctypes import *
import ctypes
from requests import request as _request

app = Flask(__name__)


class GoString(Structure):
    _fields_ = [("p", c_char_p), ("n", c_longlong)]

def gstr(str):
    return GoString(str, len(str))

@app.route("/send/<access_token>", methods=["POST"])
def send(access_token):
    dingtalk.send_robot(access_token, request.json)

@app.route("/access")
def access():
    redirect_url = request.args["redirect_to"]
    session = cdll.LoadLibrary("./session.so")
    session.Init(gstr(b"./"))
    session.Set(gstr(b"uid"), gstr(b"uid"))
    session.Set(gstr(b"uname"), gstr(b"uname"))
    session.Release()
    session.GetID.restype = GoString
    c = c_buffer("", 16)

    session_id = session.GetID()

    # data = {
    #     "user_name":"lzlin",
    #     "password":"1992.pwd.lzlin"
    # }
    # headers = {
    #     "Accept-Language":request.headers.get("Accept-Encoding"),
    #     "Accept-Language":request.headers.get("Accept-Language"),
    #     "Cache-Control":request.headers.get("Cache-Control"),
    #     "Connection":request.headers.get("Connection"),
    #     "Cookie":request.headers.get("Cookie"),
    #     "Accept":request.headers.get("Accept"),
    #     "Upgrade-Insecure-Requests":request.headers.get("Upgrade-Insecure-Requests"),
    #     "User-Agent":request.headers.get("User-Agent"),
    # }
    # resp = _request("POST",'http://git.tzyun.com/user/login', data=data, headers=headers)
    response = redirect(redirect_url)
    response.set_cookie("i_like_gogits", session_id.p)

    return response



if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)