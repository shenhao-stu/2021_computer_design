# -*- encoding: utf-8 -*-
"""
@Author             :  Hao Shen
@Last Modified by   :  Hao Shen
@Last Modified time :  2021/03/13 23:20:19
@Email              :  shenhao0223sh@gamil.com
@Describe           :  None
"""

# here put the import lib
import sys
import random
import time
import requests
import re
from parsel import Selector
from peewee import IntegrityError
from db import Ci
from db import CiAuthor

header = {
    "Connection": "keep-alive",
    "Origin": "http://qsc.zww.cn",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.3",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Referer": "http://qsc.zww.cn/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
    # "Cookie": "Hm_lvt_12506b8a4147836b0046047de09b2a2e=1493688567; _D_SID=92CED13DD066A18AEC64F1086BA2B715; ASPSESSIONIDSABSRATC=OOFAEFEAJAGIAIEMGGAEDBNL; UM_distinctid=15c6821bb13453-0fd27be8dc79a5-30657509-13c680-15c6821bb14468; CNZZDATA618132=cnzz_eid%3D761011847-1496395659-null%26ntime%3D1496395659"
}

reload(sys)
sys.setdefaultencoding('utf-8')


seek_patt = re.compile(r"\((.*?)\)", re.I | re.X)

# ---------------------------------


class QTSBase(object):

    def filllist(self, content):
        self.content = content

    def fillpage(self, fillpage):
        self.page = fillpage

    def fillbody(self, content):
        self.content = content


class ParentBase(object):

    def __init__(self):
        self.QTS = QTSBase()

# ----------------------------------


parent = ParentBase()


exec("parent.QTS.fillpage('第1页 共92页 1564条')")


def __with_seek_type__(seek_type):
    def request(pageno, value=''):
        url = 'http://qsc.zww.cn/getdata.asp'
        payload = {
            'seektype': seek_type,
            'seekvalue': value,
            'pageno': int(pageno)
        }

        resp = requests.post(
            url,
            data=payload,
            headers=header
        )

        return resp

    return request


def parse(html, callback, *args, **kwargs):
    html = html.decode('utf8')
    html = html.encode('latin1')
    html = html.decode('gb2312', 'ignore')
    sel = Selector(text=html)
    return callback(sel, *args, **kwargs)


def callback_author_list(sel, *args, **kwargs):
    data = sel.xpath('//script').extract()[0]
    for l in data.splitlines():
        if not l.startswith('parent.QTS.filllist'):
            continue

        exec(l)

        sel = Selector(
            text=unicode(parent.QTS.content)
        )

        for i in sel.xpath('//a'):
            seek = i.xpath('@onclick').extract()[0]
            seek = seek_patt.findall(seek)[0]
            _type, value, pageno = seek.split(',')
            text = i.xpath('text()').extract()[0]

            if _type != '10':
                continue

            name = text.replace('…', '')

            # save author to database.
            try:
                CiAuthor.create(
                    value=value,
                    name=name
                )
                print("key%s, has been created." % value)
            except IntegrityError:
                print("duplicate key%s, has been skipped." % value)


def callback_author_info(sel, *args, **kwargs):
    data = sel.xpath('//script').extract()[0]
    for l in data.splitlines():
        if not l.startswith('parent.QTS.fillbody'):
            continue

        exec(l)

        sel = Selector(
            text=unicode(parent.QTS.content)
        )

        ds = sel.xpath('//text()').extract()

        name = sel.xpath('//text()').extract()[1]

        lon = ''.join([s.strip() for s in ds[5:]]).strip()

        author = kwargs["author"]
        author.long_desc = lon
        #author.short_desc = sht
        author.save()
        print("key%s(%s), has been updated" % (author.value, author.name))

        return sel
    return sel


def callback_ci_info(sel, *args, **kwargs):
    data = sel.xpath('//script').extract()[0]
    for l in data.splitlines():
        if not l.startswith('parent.QTS.fillbody'):
            continue

        if '宋体' in l:
            continue

        exec(l)

        sel = Selector(
            text=unicode(parent.QTS.content)
        )

        value = kwargs["seekid"]

        rhythmic = sel.xpath('//b/text()').extract()[0]
        author = sel.xpath('//text()').extract()[1]

        contents = sel.xpath('//text()').extract()[2:]

        content = '\n'.join(contents)

        try:
            Ci.create(
                value=value,
                rhythmic=rhythmic,
                author=author,
                content=content
            )
            print("key%s, has been created." % value)
        except IntegrityError:
            Ci.update(
                rhythmic=rhythmic,
                author=author,
                content=content
            ).where(
                Ci.value == value
            ).execute()

            print("duplicate key%s, has been updated." % value)

        return sel


f_author_list = __with_seek_type__(1)
f_author_info = __with_seek_type__(10)
f_ci_list = __with_seek_type__(5)
f_ci_info = __with_seek_type__(9)


#resp = f_ci_info(1, value=1460)
#sel = parse(resp.text, callback_ci_info, seekid=1)

if __name__ == '__main__':
    for p in range(1, 93):
        resp = f_author_list(p, value=1)
        sel = parse(resp.text, callback_author_list)

    # crawl author info
    for i in CiAuthor.select().where(CiAuthor.value > 0):
        resp = f_author_info(1, value=i.value)
        sel = parse(resp.text, callback_author_info, author=i)

    # crawl author ci list
    for i in range(1, 21051):
        try:
            resp = f_ci_info(1, value=i)
        except requests.exceptions.ConnectionError as e:
            wait_seconds = random.choice(range(1, 10))
            print("waiting%s..error(%s)" % (wait_seconds, str(e)))

            time.sleep(wait_seconds)
            continue

        sel = parse(resp.text, callback_ci_info, seekid=i)
