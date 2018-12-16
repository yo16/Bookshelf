# -*- coding: utf-8 -*-
""" book flat list
List all books

2018/12/15 y.ikeda
"""

from flask import Flask, render_template, request
import re

from models import get_books

# １ページの表示件数
NUM_OF_LIST = 40


def main():
    # 表示するページと、開始要素を決める
    cur_page = 0
    if 'page' in request.args:
        str_param_page = request.args.get('page')
        if str_param_page.isdecimal():
            cur_page = int(str_param_page)

    # DBから情報を取得
    search_strs = []
    input_search_str = ''
    if 'searchStr' in request.args:
        input_search_str = request.args.get('searchStr')
        strs = re.split('\s+', input_search_str)
        for s in strs:
            search_strs.append(s.strip())
    bs, cur_page, last_page = get_books(
        search_strs=search_strs,
        page=cur_page,
        num_per_page=NUM_OF_LIST
    )

    # 表示用に諸々を整形
    for b in bs:
        title_len = 11
        if len(b['title'])>title_len:
            b['title'] = b['title'][:title_len] + '...'

    # 前のページ、次のページ番号を決める
    prev_page = -1
    if 0 < cur_page:
        prev_page = cur_page - 1
    next_page = -1
    if cur_page < last_page:
        next_page = cur_page + 1

    # ページ情報
    page_info = {
        'prev': prev_page,
        'cur': cur_page,
        'next': next_page,
        'last': last_page
    }
    #print(page_info)
    #print(bs)

    return render_template(
        'flatBookList.html',
        books=bs,
        page=page_info,
        search_str=input_search_str,
        base_page='flatList'
    )

