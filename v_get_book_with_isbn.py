# -*- coding: utf-8 -*-
""" get_book_with_isbn
Get book info with using isbn-code.
"""

import urllib
import urllib2
from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup, BeautifulStoneSoup
from bookshelf_common import APP_DOMAIN

#from google.appengine.ext import ndb
import json

from models import Books, Book, Publisher, Tag


def main(request):
    isbn = request.json['isbn']

    ret_dic = {
        'isbn': '',
        'title': '',
        'authors': [],
        'publisher': '',
        'publisher_code': '',
        'image_url': '',
        'comment': '',
        'tags': []
    }

    # Datastoreを優先に探す
    b = Book.get_book_by_isbn(isbn)
    if b is not None:
        # Datastoreに登録されている場合は、その値を表示
        ret_dic['isbn'] = isbn
        ret_dic['title'] = b.title
        ret_dic['authors'] = []
        for a in b.authors:
            ret_dic['authors'].append(a)
        #p_key = ndb.Key(Publisher, b.publisher_key_id)
        p = Publisher.get_publisher_by_id(b.publisher_key_id)
        if p is None:
            ret_dic['publisher'] = '[code]' + slice_publisher_code(isbn)
        else:
            ret_dic['publisher'] = p.pub_name
        ret_dic['publisher_code'] = slice_publisher_code(isbn)
        ret_dic['publisher_key_id'] = b.publisher_key_id
        ret_dic['image_url'] = b.image_url
        ret_dic['comment'] = b.comment
        tags_str = ''
        i = 0
        for t_id in b.tags:
            if i>0:
                tags_str += ', '
            # Tagから文字列へ変換
            t = Tag.get_tag_by_id(t_id)
            tags_str += t.tag_name
            i += 1
        ret_dic['tags'] = tags_str
    else:
        # Datastoreに登録されていない場合は、
        # Googleから情報を取得（出版社以外）
        ret_dic = get_by_GoogleApi(isbn)

        # 出版社を取得
        publisher, publisher_key_id = get_publisher(isbn)
        ret_dic['publisher'] = publisher
        ret_dic['publisher_code'] = slice_publisher_code(isbn)
        ret_dic['publisher_key_id'] = publisher_key_id
    
    if (ret_dic['image_url'] is None) or (len(ret_dic['image_url'])==0):
        ret_dic['image_url'] = '/static/img/NoImage.png'

    return jsonify(ResultSet=json.dumps(ret_dic))


def get_by_GoogleApi(isbn):
    """ Get book info by GoogleAPI
    """
    ret = {
        'title': '',
        'authors': [],
        'isbn': '',
        'thumbnail': '',
        'image_url': ''
    }

    #url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:' + isbn + '&key=' + API_KEY
    #url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:' + isbn + '&country=JP&key=' + API_KEY
    url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:' + isbn + '&country=JP'
    #https://www.googleapis.com/books/v1/volumes?q=isbn:9784873117584&key=AIzaSyAt1d-a2u44JOMOj5iYI3LzpwISkasj0is
    print 'URL:', url
    headers = {
        'Referer': APP_DOMAIN,
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0'
    }
    opener = urllib2.build_opener()
    opener.addheaders = [
        ('Referer',APP_DOMAIN),
        ('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0')
    ]
    try:
        #instance = urllib2.urlopen(url)
        instance = opener.open(url)
    except urllib2.HTTPError as err:
        print '*** urllib2.HTTPError ***'
        print err.code
        print err.reason
        raise
    except urllib2.URLError as err:
        print '*** urllib2.URLError ***'
        print err.reason
        raise

    soup = BeautifulSoup(instance, 'html5lib', fromEncoding='utf-8')
    body = soup.select_one('body').text
    jdata = json.loads(body)

    got_num = jdata['totalItems']
    if got_num < 1:
        return ret

    # Googleから取得した情報を設定
    item = jdata['items'][0]
    ret['title'] = item['volumeInfo']['title']
    if 'authors' in item['volumeInfo']:
        for a in item['volumeInfo']['authors']:
            ret['authors'].append(a)
    if 'imageLinks' in item['volumeInfo']:
        thumbnail = item['volumeInfo']['imageLinks']['thumbnail']
        ret['image_url'] = 'https' + thumbnail[len('http'):]
    ret['isbn'] = isbn

    return ret


def get_publisher(isbn):
    """ 出版者とIDを取得する
    """
    # Datastoreから、出版社を取得
    publisher_name, publisher_key_id = get_publisher_from_datastore(isbn)

    # Datastoreで見つからなかった場合は、ISBN公式サイトから取得
    if publisher_name is None:
        # ISBNサイトから、出版社を取得
        #publisher_name = get_publisher_from_isbn(isbn)        # 未実装のためコメントアウト
        publisher_name = '[code]' + slice_publisher_code(isbn)  # ダミーコード
        if publisher_name is None:
            # 見つからない場合は、定形文を書いておく
            publisher_name = '[code]' + slice_publisher_code(isbn)
        # 次回のためにDatastoreへ保存しておく
        publisher_key_id = put_publisher_into_datastore(slice_publisher_code(isbn), publisher_name)
    
    return publisher_name, publisher_key_id


def get_publisher_from_datastore(isbn):
    """ Get Publisher from datastore
    """
    isbn_pub = slice_publisher_code(isbn)

    pub_name = None
    pub_id = None
    q = Publisher.query(Publisher.pub_code == isbn_pub).get()
    if q is not None:
        pub_name = q.pub_name
        pub_id = q.key.integer_id()

    return pub_name, pub_id


def get_publisher_from_isbn(isbn):
    """ Get Publisher from ISBN
    """
    ret_publisher = ''

    # 13桁のISBN以外はとりあえず非対応
    if len(isbn)<13:
        return ''
    
    # 出版者コード
    isbn_pub = slice_publisher_code(isbn)
    print '  isbn-code:' + isbn_pub

    url = 'https://isbn.jpo.or.jp/index.php/fix__ref_pub/'
    params = urllib.urlencode({
        'kensakuvalue': isbn_pub,
        'snonce': '40010362f8'
    })
    req = urllib2.Request(url, params)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36')
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    req.add_header('Host', 'isbn.jpo.or.jp')
    req.add_header('Origin','https://isbn.jpo.or.jp')
    req.add_header('Referer','https://isbn.jpo.or.jp/index.php/fix__ref_pub/')
    instance = urllib2.urlopen(req)
    soup = BeautifulSoup(instance, fromEncoding='utf-8')
    tbl = soup.select_one('#tblp1')
    print type(tbl)
    print tbl
    if tbl is None:
        print 'None table'
        return (None, None)
    trs = tbl.find_all('tr')
    if trs is None:
        return (None, None)
    if len(trs)<2:
        return (None, None)
    tds = trs[1].find_all('td')
    if tds is None:
        return (None, None)

    return (isbn_pub, ret_publisher)


def put_publisher_into_datastore(code, name):
    """ Put publisher info into Datastore
    """
    isbn_info = {
        'pub_code': code,
        'pub_name': name
    }
    pub_key = Publisher(**isbn_info).put()
    return pub_key.integer_id()


def slice_publisher_code(isbn):
    """ 出版社コードを抜き出して返す
    """
    top2 = int(isbn[4:6])
    keta = 2
    if top2 < 20:
        keta = 2
    elif top2 < 70:
        keta = 3
    elif top2 < 85:
        keta = 4
    elif top2 < 90:
        keta = 5
    elif top2 < 95:
        keta = 6
    else:
        keta = 7
    return isbn[4:4+keta]
