# -*- coding: utf-8 -*-
""" regist_book
Regist new book.
"""

from flask import Flask, render_template, request

from models import Book, Tag
import v_booklist

def main():
    book_info = {
        'isbn': request.form['isbn'],
        'title': request.form['title'],
        'authors': [],
        'publisher': request.form['publisher'],
        'image_url': request.form['image_url'],
        'comment': request.form['comment'],
        'tags': []
    }
    print('---------')
    print(book_info)
    # authors0, authors1, authors2, ・・・
    num_of_authors = int(request.form['num_of_authors'])
    for i in range(num_of_authors):
        book_info['authors'].append(request.form['author'+str(i)])
    # tags
    tags_entered = request.form['tags'].split(',')
    for tag in tags_entered:
        reg_tag = {'tag_name': tag.strip()}
        # Tagを問い合わせて、無かったら登録
        t = Tag.query(Tag.tag_name==reg_tag['tag_name']).get()
        tag_key = None
        if t is None:
            # 登録
            tag_key = Tag(**reg_tag).put()
            #t = Tag.query(Tag.tag_name==reg_tag['tag_name']).get()
        else:
            # あったらキーを返す
            tag_key = t.key
        
        #print('t.id:', tag_key.integer_id())
        cur_id = tag_key.integer_id()
        book_info['tags'].append(cur_id)

    # 問い合わせてなかったら登録
    b = Book.query(Book.isbn==book_info['isbn']).get()
    if b is None:
        # 登録
        Book(**book_info).put()
    else:
    # あったら更新
        b.title = book_info['title']
        b.authors = []
        for a in book_info['authors']:
            b.authors.append(a)
        b.publisher = book_info['publisher']
        b.image_url = book_info['image_url']
        b.comment = book_info['comment']
        b.tags = []
        for t in book_info['tags']:
            b.tags.append(t)

        #for k, v in book_info.items():
        #    setattr(b, k, v)
        #    #b[k] = v
        b.put()

    return v_booklist.main()

