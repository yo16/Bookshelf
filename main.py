# -*- coding: utf-8 -*-
"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask, request, jsonify
app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

import os
import sys
#print(sys.path)
#print(os.getcwd())

import v_booklist
import v_enter_new_book
import v_get_book_with_isbn
import v_regist_book


@app.route('/')
def index():
    """Return Books list."""
    return v_booklist.main()

@app.route('/enter_new_book')
def regist():
    """Enter new book info."""
    return v_enter_new_book.main()

@app.route('/get_book_with_isbn', methods=['POST'])
def get_book_with_isbn():
    """Get book info"""
    if request.headers['Content-Type'] != 'application/json':
        print(request.headers['Content-Type'])
        return jsonify(res='error'), 400
    
    return v_get_book_with_isbn.main(request)

@app.route('/regist', methods=['POST'])
def regist_book():
    """Regist book"""
    return v_regist_book.main()



@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404

@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500


#if __name__=='__main__':
#    app.run(debug=True)
