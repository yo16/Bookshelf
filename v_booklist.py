""" booklist
List all books

2018/11/10 y.ikeda
"""

from flask import Flask, render_template, request

from models import Books, Book, Tag
from google.appengine.ext import ndb


def main():
    # Get infos from Datastore.
    #bs = get_books()
    #print "----------"
    q = Book.query()
    #q = ndb.Query(Book)
    print q
    bs_db = q.fetch()
    #print bs
    #print "type", type(bs)
    bs = []
    for b in bs_db:
        cur_book = {}
        cur_book['title'] = b.title
        cur_book['authors'] = []
        for a in b.authors:
            cur_book['authors'].append(a)
        cur_book['publisher'] = b.publisher
        cur_book['isbn'] = b.isbn
        cur_book['image_url'] = b.image_url
        cur_book['comment'] = b.comment
        cur_book['tags'] = []
        for t_keyid in b.tags:
            tag_key = ndb.Key(Tag, t_keyid)
            t = tag_key.get()
            cur_book['tags'].append(t.tag_name)
        bs.append(cur_book)
    
    return render_template(
        'booklist.html',
        books=bs
    )

def get_books():
    #return [{'title': 'test'}]
    bs = Books()
    blist = bs.get_books()
    return blist

