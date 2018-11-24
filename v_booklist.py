""" booklist
List all books

2018/11/10 y.ikeda
"""

from flask import Flask, render_template, request

from models import Books, Book
from google.appengine.ext import ndb


def main():
    # Get infos from Datastore.
    #bs = get_books()
    #print "----------"
    q = Book.query()
    #q = ndb.Query(Book)
    print q
    bs = q.fetch()
    print bs
    print "type", type(bs)
    
    return render_template(
        'booklist.html',
        books=bs
    )

def get_books():
    #return [{'title': 'test'}]
    bs = Books()
    blist = bs.get_books()
    return blist

