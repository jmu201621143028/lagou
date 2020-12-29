import requests
import time
import math
from decrypt import getcookiesfromchrome
import urllib.request as urllib_request
'''
    https://stackoverflow.com/questions/60416350/chrome-80-how-to-decode-cookies
'''


def sendpost(url, data):
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,zh;q=0.8,zh-CN;q=0.7',
        'content-length': '247',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://easy.lagou.com',
        'referer': 'https://easy.lagou.com/talent/search/list.htm',
        'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'x-anit-forge-code': '',
        'x-anit-forge-token': '',
        'x-requested-with': 'XMLHttpRequest'
    }
    host = 'lagou'
    cookies = getcookiesfromchrome(host)
    num = 0
    while num < 5:
        req = requests.post(url, data=data, headers=headers, cookies=cookies)
        ans = req.json()
        time.sleep(0.5)
        num += 1
        if ans['state'] == 1:
            return ans
        else:
            cookies = getcookiesfromchrome(host)
    return None


def main():
    url = r"https://easy.lagou.com/talent/search/list.json"
    data = {'keyword': 'MFC', 'city': '深圳',
            'pageNo': '1', 'education': '不限', 'sex': '不限', 'isEliteSchool': '1', 'workYear': '1年-3年', 'age': '不限',
            'industryField': '不限', 'expectSalary': '不限', 'searchVersion': '1'}
    staff = sendpost(url, data)
    if staff is None:
        print("请刷新后重试")
        return
    staff = staff['content']['data']['page']
    pagenum = math.ceil(staff['totalCount'] / staff['pageSize'])
    for i in range(pagenum):
        data['pageNo'] = str(i+1)
        url = r"https://easy.lagou.com/talent/search/list.json"
        staff = sendpost(url, data)
        staff = staff['content']['data']['page']
        haschat = {}
        encrypeId = [i['encryptUserId'] for i in staff['result']]
        haschat['cUserIds'] = ','.join(encrypeId)
        haschat['type'] = "SEARCH"
        url = r"https://easy.lagou.com/talent/search/deliverInfo.json"
        res = sendpost(url, haschat)
        chat = res['content']['rows']
        for name in chat:
            if not name['hasChat']:
                url = r'https://easy.lagou.com/im/session/batchCreate/{}.json'.format(name['userId'])
                para = {'greetingId': '1750568_b_1', 'positionId': '7809818', 'inviteDeliver': 'true'}
                res = sendpost(url, para)
                if res is None:
                    print("error")
                else:
                    print("success")
            else:
                print("had success")


if __name__ == '__main__':
    main()
