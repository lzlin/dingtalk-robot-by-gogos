# -*- coding:utf-8 –*-
from requests import request
import urllib

dingtalk_robot_url = "https://oapi.dingtalk.com/robot/send?access_token=%s"

domian = "git.tzyun.com"


def send_robot(access_token, data):
    url = data.get("compare_url", "")
    if not url:
        url = data["commits"][0]["url"]

    json = {
        "actionCard": {
            "title": "乔布斯 20 年前想打造一间苹果咖啡厅，而它正是 Apple Store 的前身",
            "text": '''![screenshot](@lADOpwk3K80C0M0FoA)
     ### 乔布斯 20 年前想打造的苹果咖啡厅
     Apple Store 的设计正从原来满满的科技感走向生活化，而其生活化的走向其实可以追溯到 20 年前苹果一个建立咖啡馆的计划''',
            "hideAvatar": "0",
            "btnOrientation": "0",
            "singleTitle": "查看详情",
            "singleURL": "http://%s/access/%s" % (domian, urllib.quote(url.encode("utf8")))
        },
        "msgtype": "actionCard"
    }


    return  request("POST", dingtalk_robot_url % access_token, json=json)