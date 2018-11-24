# -*- coding: utf-8 -*-
""" enter_new_book
Show for enter new book infos.
"""

from flask import Flask, render_template, request

from models import Books, Book
from google.appengine.ext import ndb

def main():
    return render_template('enter_new_book.html')
