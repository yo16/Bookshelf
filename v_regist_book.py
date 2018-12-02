# -*- coding: utf-8 -*-
""" regist_book
Regist new book.
"""

from flask import Flask, render_template, request

from models import regist_book
import v_booklist

def main():
    # Book登録用のdictionaryを作る
    book_info = {
        'isbn': request.form['isbn'],
        'title': request.form['title'],
        'authors': [],
        'publisher_key_id': request.form['publisher_key_id'],
        'image_url': request.form['image_url'],
        'comment': request.form['comment'],
        'tag_names': []
    }
    # authors0, authors1, authors2, ・・・
    num_of_authors = int(request.form['num_of_authors'])
    for i in range(num_of_authors):
        book_info['authors'].append(request.form['author'+str(i)])
    # publisher_key_id
    if len(book_info['publisher_key_id'])==0:
        book_info['publisher_key_id'] = None
    else:
        book_info['publisher_key_id'] = int(book_info['publisher_key_id'])
    # tagnames
    tags_entered = request.form['tags'].split(',')
    for tag in tags_entered:
        reg_tag_name = tag.strip()
        if len(reg_tag_name)==0:
            continue
        book_info['tag_names'].append(reg_tag_name)
    # image_url
    if (book_info['image_url'] is None) or (len(book_info['image_url'])==0):
        book_info['image_url'] = '/static/img/NoImage.png'
    print(book_info)

    # 登録
    regist_book(book_info)

    return v_booklist.main()

