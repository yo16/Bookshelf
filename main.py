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
import v_maintenance
import v_csv_output
import v_csv_input
import v_bookflatlist


@app.route('/')
def index():
    """Return Books list."""
    return v_booklist.main()

@app.route('/flatList')
def flat_list():
    """Flat List"""
    return v_bookflatlist.main()

@app.route('/enterNewBook', methods=['GET'])
def regist():
    """Enter new book info."""
    return v_enter_new_book.main()

@app.route('/getBookWithIsbn', methods=['POST'])
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

@app.route('/maintenance')
def maintenance():
    """Maintenance"""
    return v_maintenance.main()

@app.route('/outputCsv')
def output_csv():
    """Output CSV"""
    return v_csv_output.main()

@app.route('/inputCsv', methods=['POST'])
def input_csv():
    """Input CSV"""
    return v_csv_input.main()


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
