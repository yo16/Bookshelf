# -*- coding: utf-8 -*-
""" enter_new_book
Show for enter new book infos.
"""

from flask import Flask, render_template, request


def main():
    isbn=''
    if 'isbn' in request.args:
        isbn = request.args.get('isbn')
    return render_template(
        'enterNewBook.html',
        isbn=isbn
    )
