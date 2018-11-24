# -*- coding: utf-8 -*-
""" regist_book
Regist new book.
"""

from flask import Flask, render_template, request

from models import Book
import v_booklist

def main():
    book_info = {
        'isbn': request.form['isbn'],
        'title': request.form['title'],
        'authors': [],
        'publisher': request.form['publisher'],
        'image_url': request.form['image_url'],
        'comment': request.form['comment']
    }
    num_of_authors = int(request.form['num_of_authors'])
    for i in range(num_of_authors):
        book_info['authors'].append(request.form['author'+str(i)])

    # 問い合わせてなかったら登録
    b = Book.query(Book.isbn==book_info['isbn']).get()
    if b is None:
        # 登録
        Book(**book_info).put()
    else:
    # あったら更新
        for k, v in book_info.items():
            setattr(b, k, v)
        b.put()

    return v_booklist.main()

