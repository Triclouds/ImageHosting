'''
cron: 0 5 8-22 * * *
new Env('f充值购买');
活动入口微信打开：http://2478987.epghgkvalp.wjbk.25obcxyume.cloud/?p=2478987
下载地址：https://www.123pan.com/s/xzeSVv-IHpfv.html
公告地址：http://175.24.153.42:8881/getmsg?type=czgm

使用方法：
1.活动入口,微信打开：http://2478987.epghgkvalp.wjbk.25obcxyume.cloud/?p=2478987
2.打开活动入口，抓包的任意接口cookies中的gfsessionid参数,
3.青龙环境变量菜单，添加本脚本环境变量
名称 ：czgm_config
单个账户参数： ['name|ck|key|uids']
例如：['账号1|729ac1356xxxxb7407bd2ea|keykeykey|uid_xxxxx']
多个账户['name|ck|key|uids','name|ck|key|uids','name|ck|key|uids']
例如：['账号1|729ac1356xxxxb7407bd2ea|keykeykey|uid_xxxxx','账号2|729ac1356xxxxb7407bd2ea|keykeykey|uid_xxxxx','账号3|729ac1356xxxxb7407bd2ea|keykeykey|uid_xxxxx']
参数说明与获取：
ck:打开活动入口，抓包的任意接口cookies中的gfsessionid参数
key:每个账号的推送标准，每个账号全阅读只需要一个key,多个账号需要多个key,key永不过期。
为了防止恶意调用key接口，限制每个ip每天只能获取一个key。手机开飞行模式10s左右可以变更ip重新获取key
通过浏览器打开链接获取:http://175.24.153.42:8882/getkey
uids:wxpusher的参数，当一个微信关注了一个wxpusher的推送应用后，会在推送管理后台(https://wxpusher.zjiecode.com/admin/main)的'用户管理-->用户列表'中显示
用户在推送页面点击’我的-->我的UID‘也可以获取

4.青龙环境变量菜单，添加本脚wxpusher环境变量
青名称 ：push_config
参数 ：{"printf":0,"threadingf":1,"appToken":"xxxx"}
例如：{"printf":0,"threadingf":1,"appToken":"AT_r1vNXQdfgxxxxxscPyoORYg"}
参数说明：
printf 0是不打印调试日志，1是打印调试日志
threadingf:并行运行账号参数 1并行执行，0顺序执行，并行执行优点，能够并行跑所以账号，加快完成时间，缺点日志打印混乱。
appToken 这个是填wxpusher的appToken

5.提现标准默认是3000，与需要修改，请在本脚本最下方，按照提示修改

'''
import threading
import time
import hashlib
import requests
import random
import re
import json
import os

checkDict = {
    'MzkyMzI5NjgxMA==': ['每天趣闻事', ''],
    'MzkzMzI5NjQ3MA==': ['欢闹青春', ''],
    'Mzg5NTU4MzEyNQ==': ['推粉宝助手', ''],
    'Mzg3NzY5Nzg0NQ==': ['新鲜事呦', ''],
    'MzU5OTgxNjg1Mg==': ['动感比特', ''],
    'Mzg4OTY5Njg4Mw==': ['邻居趣事闻', 'gh_60ba451e6ad7'],
    'MzI1ODcwNTgzNA==': ['麻辣资讯', 'gh_1df5b5259cba'],
}


def getmsg():
    lvsion = 'v1.3f'
    r = ''
    try:
        u = 'http://175.24.153.42:8881/getmsg'
        p = {'type': 'czgm'}
        r = requests.get(u, params=p)
        rj = r.json()
        version = rj.get('version')
        gdict = rj.get('gdict')
        gmmsg = rj.get('gmmsg')
        print('系统公告:', gmmsg)
        print(f'最新版本{version}当前版本{lvsion}')
        print(f'系统的公众号字典{len(gdict)}个:{gdict}')
        print(f'本脚本公众号字典{len(checkDict.values())}个:{list(checkDict.keys())}')
        print('=' * 50)
    except Exception as e:
        print(r.text)
        print(e)
        print('公告服务器异常')


def push(title, link, text, type1, uids, key):
    str1 = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>TITLE</title>
<style type=text/css>
   body {
   	background-image: linear-gradient(120deg, #fdfbfb 0%, #a5d0e5 100%);
    background-size: 300%;
    animation: bgAnimation 6s linear infinite;
}
@keyframes bgAnimation {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
</style>
</head>
<body>
<p>TEXT</p><br>
<p><a href="http://175.24.153.42:8882/lookstatus?key=KEY&type=TYPE">查看状态</a></p><br>
<p><a href="http://175.24.153.42:8882/lookwxarticle?key=KEY&type=TYPE&wxurl=LINK">点击阅读检测文章</a></p><br>
</body>
</html>
    '''
    content = str1.replace('TITTLE', title).replace('LINK', link).replace('TEXT', text).replace('TYPE', type1).replace(
        'KEY', key)
    datapust = {
        "appToken": appToken,
        "content": content,
        "summary": title,
        "contentType": 2,
        "uids": [uids]
    }
    urlpust = 'http://wxpusher.zjiecode.com/api/send/message'
    try:
        p = requests.post(url=urlpust, json=datapust).text
        print(p)
        return True
    except:
        print('推送失败！')
        return False


def sha_256(text):
    hash = hashlib.sha256()
    hash.update(text.encode())
    t = hash.hexdigest()
    return t


def getinfo(link):
    try:
        r = requests.get(link)
        # print(r.text)
        html = re.sub('\s', '', r.text)
        biz = re.findall('varbiz="(.*?)"\|\|', html)
        if biz != []:
            biz = biz[0]
        if biz == '' or biz == []:
            if '__biz' in link:
                biz = re.findall('__biz=(.*?)&', link)
                if biz != []:
                    biz = biz[0]
        nickname = re.findall('varnickname=htmlDecode\("(.*?)"\);', html)
        if nickname != []:
            nickname = nickname[0]
        user_name = re.findall('varuser_name="(.*?)";', html)
        if user_name != []:
            user_name = user_name[0]
        msg_title = re.findall("varmsg_title='(.*?)'\.html\(", html)
        if msg_title != []:
            msg_title = msg_title[0]
        text = f'公众号唯一标识：{biz}|文章:{msg_title}|作者:{nickname}|账号:{user_name}'
        print(text)
        return nickname, user_name, msg_title, text, biz
    except Exception as e:
        print(e)
        print('异常')
        return False


class HHYD():
    def __init__(self, cg):
        print(cg)
        self.name = cg[0]
        self.ck = cg[1]
        self.key = cg[2]
        self.uids = cg[3]
        self.headers = {
            'Host': '2478987.jilixczlz.ix47965in5.cloud',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090621) XWEB/8351 Flue',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh',
            'Cookie': f'gfsessionid={self.ck}',
        }
        self.sec = requests.session()
        self.sec.headers = self.headers

    def printjson(self, text):
        if printf == 0:
            return
        print(self.name, text)

    def setstatus(self):
        try:
            u = 'http://175.24.153.42:8882/setstatus'
            p = {'key': self.key, 'type': 'czgm', 'val': '1'}
            r = requests.get(u, params=p,timeout=10)
            print(self.name, r.text)
        except Exception as e:
            print('设置状态异常')
            print(e)

    def getstatus(self):
        try:
            u = 'http://175.24.153.42:8882/getstatus'
            p = {'key': self.key, 'type': 'czgm'}
            r = requests.get(u, params=p,timeout=3)
            return r.text
        except Exception as e:
            print('查询状态异常',e)
            return False

    def user_info(self):
        ts = int(time.time())
        text = f'key=4fck9x4dqa6linkman3ho9b1quarto49x0yp706qi5185o&time={ts}'
        sign = sha_256(text)
        u = f'http://2478987.jilixczlz.ix47965in5.cloud/user/info?time={ts}&sign={sign}'
        r = ''
        try:
            r = self.sec.get(u)
            rj = r.json()
            if rj.get('code') == 0:
                print(self.name, f'用户UID:{rj.get("data").get("uid")}')
                return True
            else:
                print(self.name, f'获取用户信息失败，账号异常')
                return False
        except:
            print(self.name, r.text)
            print(self.name, f'获取用户信息失败,gfsessionid无效，请检测gfsessionid是否正确')
            return False

    def msg(self):
        r = ''
        try:
            ts = int(time.time())
            text = f'key=4fck9x4dqa6linkman3ho9b1quarto49x0yp706qi5185o&time={ts}'
            sign = sha_256(text)
            u = f'http://2478987.jilixczlz.ix47965in5.cloud/user/msg?time={ts}&sign={sign}'
            r = self.sec.get(u)
            rj = r.json()
            print(self.name, f'系统公告:{rj.get("data").get("msg")}')
        except:
            print(self.name, r.text)
            return False

    def read_info(self):
        r = ''
        try:
            ts = int(time.time())
            text = f'key=4fck9x4dqa6linkman3ho9b1quarto49x0yp706qi5185o&time={ts}'
            sign = sha_256(text)
            u = f'http://2478987.jilixczlz.ix47965in5.cloud/read/info?time={ts}&sign={sign}'
            r = self.sec.get(u)
            rj = r.json()
            self.remain = rj.get("data").get("remain")
            print(self.name,
                  f'今日已经阅读了{rj.get("data").get("read")}篇文章，今日总金币{rj.get("data").get("gold")}，剩余{self.remain}')
        except:
            print(self.name, r.text)
            return False

    def read(self):
        print(self.name, '阅读开始')
        while True:
            print(self.name, '-' * 50)
            ts = int(time.time())
            text = f'key=4fck9x4dqa6linkman3ho9b1quarto49x0yp706qi5185o&time={ts}'
            sign = sha_256(text)
            u = f'http://2478987.jilixczlz.ix47965in5.cloud/read/task?time={ts}&sign={sign}'
            r = self.sec.get(u)
            self.printjson(r.text)
            rj = r.json()
            code = rj.get('code')
            if code == 0:
                uncode_link = rj.get('data').get('link')
                print(self.name, '获取到阅读链接成功')
                link = uncode_link.encode().decode()
                a = getinfo(link)
                if self.testCheck(a, link) == False:
                    return False
                sleeptime = random.randint(7, 10)
                print(self.name, '本次模拟阅读', sleeptime, '秒')
                time.sleep(sleeptime)
            elif code == 400:
                print(self.name, '未知情况400')
                time.sleep(10)
                continue
            elif code == 20001:
                print(self.name, '未知情况20001')
            else:
                print(self.name, rj.get('message'))
                return False
            # -----------------------------
            self.msg()
            ts = int(time.time())
            finish_headers = self.sec.headers.copy()
            finish_headers.update({'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
                                   'Origin': 'http://2478987.jilixczlz.ix47965in5.cloud'})
            text = f'key=4fck9x4dqa6linkman3ho9b1quarto49x0yp706qi5185o&time={ts}'
            sign = sha_256(text)
            p = f'time={ts}&sign={sign}'
            u = f'http://2478987.jilixczlz.ix47965in5.cloud/read/finish'
            r = requests.post(u, headers=finish_headers, data=p)
            self.printjson(r.text)
            rj = r.json()
            if rj.get('code') == 0:
                if rj.get('data').get('check') == False:
                    gain = rj.get('data').get('gain')
                    self.remain = rj.get("data").get("remain")
                    print(self.name, f"阅读文章成功获得{gain}金币")
                    print(self.name,
                          f'当前已经阅读了{rj.get("data").get("read")}篇文章，今日总金币{rj.get("data").get("gold")}，剩余{self.remain}')
                else:
                    print(self.name, "过检测成功")
                    print(self.name,
                          f'当前已经阅读了{rj.get("data").get("read")}篇文章，今日总金币{rj.get("data").get("gold")}，剩余{self.remain}')
            else:
                return False
            time.sleep(1)
            print(self.name, '开始本次阅读')

    def testCheck(self, a, link):
        if checkDict.get(a[4]) != None:
            self.setstatus()
            for i in range(60):
                if i % 30 == 0:
                    push(f'{self.name}:充值购买过检测', link, a[3], 'czgm',self.uids,self.key)
                getstatusinfo = self.getstatus()
                if getstatusinfo == '0':
                    print(self.name, '过检测文章已经阅读')
                    return True
                elif getstatusinfo == '1':
                    print(self.name, f'正在等待过检测文章阅读结果{i}秒。。。')
                    time.sleep(1)
                else:
                    print(self.name, '服务器异常')
                    return False
            print(self.name, '过检测超时中止脚本防止黑号')
            return False
        else:
            return True

    def withdraw(self):
        if self.remain < txbz:
            print(self.name, '没有达到提现标准')
            return False
        ts = int(time.time())
        text = f'key=4fck9x4dqa6linkman3ho9b1quarto49x0yp706qi5185o&time={ts}'
        sign = sha_256(text)
        u = f'http://2478987.84.8agakd6cqn.cloud/withdraw/wechat?time={ts}&sign={sign}'
        r = self.sec.get(u, headers=self.headers)
        print(self.name, '提现结果', r.text)

    def run(self):
        self.user_info()
        self.msg()
        self.read_info()
        self.read()
        time.sleep(5)
        self.withdraw()


if __name__ == '__main__':
    pushconfig = os.getenv('push_config')
    if pushconfig == None:
        print('请检查你的推送变量名称是否填写正确')
        exit(0)
    try:
        pushconfig = json.loads(pushconfig.replace("'", '"'))
    except Exception as e:
        print(e)
        print(pushconfig)
        print('请检查你的推送变量参数是否填写正确')
        exit(0)
    czgmconfig = os.getenv('czgm_config')
    if czgmconfig == None:
        print('请检查你的充值购买脚本变量名称是否填写正确')
        exit(0)
    try:
        czgmconfig = json.loads(czgmconfig.replace("'", '"'))
    except Exception as e:
        print(e)
        print(czgmconfig)
        print('请检查你的充值购买脚本变量参数是否填写正确')
        exit(0)
    printf = pushconfig['printf']
    appToken = pushconfig['appToken']
    threadingf=pushconfig['threadingf']
    getmsg()
    txbz = 3000  # 这里是提现标志3000代表3毛
    tl = []
    if threadingf == 1:
        for i in czgmconfig:
            cg=i.split('|')
            print('*' * 50)
            print(f'开始执行{i[0]}')
            api = HHYD(cg)
            t = threading.Thread(target=api.run, args=())
            tl.append(t)
            t.start()
            time.sleep(0.5)
        for t in tl:
            t.join()
    elif threadingf == 0:
        for i in czgmconfig:
            cg = i.split('|')
            print('*' * 50)
            print(f'开始执行{cg[0]}')
            api = HHYD(cg)
            api.run()
            print(f'{cg[0]}执行完毕')
            time.sleep(3)
    else:
        print('请确定推送变量中threadingf参数是否正确')
    print('全部账号执行完成')
