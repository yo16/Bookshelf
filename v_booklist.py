# -*- coding: utf-8 -*-
""" booklist
List all books

2018/11/10 y.ikeda
"""

from flask import Flask, render_template, request

from models import Books, Book, Tag, Publisher
from google.appengine.ext import ndb

# １ページの表示件数
NUM_OF_LIST = 10


def main():
    # Datastoreから情報を取得
    q = Book.query()
    bs_db = q.fetch()

    # 表示するページを決める
    cur_page = 0
    last_page = int(len(bs_db) / NUM_OF_LIST)
    if 'page' in request.args:
        str_param_page = request.args.get('page')
        if str_param_page.isdecimal():
            cur_page = int(str_param_page)
            if cur_page < 0:
                cur_page = 0
    if len(bs_db) <= cur_page * NUM_OF_LIST:
        # データ量を超えたページ指定の場合は最終ページ
        cur_page = last_page
    # 前のページ、次のページ番号も決める
    prev_page = -1
    if 0 < cur_page:
        prev_page = cur_page - 1
    next_page = -1
    if cur_page < last_page:
        next_page = cur_page + 1

    # fetchした結果を、ページングするデータだけに絞る
    start_item = cur_page * NUM_OF_LIST
    end_item = start_item + NUM_OF_LIST - 1
    bs_db = bs_db[start_item : end_item+1]

    bs = []
    for b in bs_db:
        cur_book = {}
        cur_book['title'] = b.title
        cur_book['authors'] = []
        for a in b.authors:
            cur_book['authors'].append(a)
        cur_book['publisher'] = get_publisher(b.publisher_key_id)
        cur_book['isbn'] = b.isbn
        if (b.image_url is None) or (len(b.image_url)==0):
            b.image_url = '/static/img/NoImage.png'
        cur_book['image_url'] = b.image_url
        cur_book['comment'] = b.comment
        cur_book['tags'] = []
        for t_keyid in b.tags:
            tag_key = ndb.Key(Tag, t_keyid)
            t = tag_key.get()
            cur_book['tags'].append(t.tag_name)
        bs.append(cur_book)
    
    # ページ情報
    page_info = {
        'prev': prev_page,
        'cur': cur_page,
        'next': next_page,
        'last': last_page
    }
    #print(page_info)

    return render_template(
        'booklist.html',
        books=bs,
        page=page_info
    )

def get_books():
    #return [{'title': 'test'}]
    bs = Books()
    blist = bs.get_books()
    return blist

def get_publisher(id):
    """publisher_key_idからpublisherを取得
    """
    p_key = ndb.Key(Publisher, id)
    if p_key is None:
        return ""
    
    publisher = p_key.get()
    return publisher.pub_name
