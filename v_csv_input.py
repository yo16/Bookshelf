# -*- coding: utf-8 -*-
""" v_csv_input
DataStoreのデータをCSV入力
"""
from flask import Flask, render_template, request, send_file
from pathlib import Path
import datetime
import zipfile
from io import StringIO, BytesIO
import csv
from werkzeug import secure_filename

import v_maintenance
from models import regist_book, regist_publisher

def main():
    # CSVのタイプを取得
    file_type = request.form['file_type']
    if file_type=='Book':
        regist_book_csv()
    elif file_type=='Publisher':
        regist_publisher_csv()
    
    return v_maintenance.main()


def regist_book_csv():
    """ bookのcsvを登録
    """
    f = request.files['csv_file']
    filename = secure_filename(f.filename)
    ext = Path(filename).suffix
    if ext != '.csv':
        return v_maintenance.main()

    # CSVファイルを読み込む
    row_index = -1
    csv_data = []
    csv_columns = ['title','publisher','authors','comment','tag_names','isbn','image_url']
    for l in f:
        row_index += 1
        if row_index==0:
            # １行目はヘッダ
            #raw_col_names = l.split(',')
            #for raw_col in raw_col_names:
            #    csv_columns.append(
            #        strip_double_quote(raw_col)
            #    )
            continue

        row_csv = l.split(',')
        if len(row_csv) != len(csv_columns):
            continue
        row_csv_strip = {}
        for i, col in enumerate(row_csv):
            row_csv_strip[csv_columns[i]] = strip_double_quote(col)
        # authors
        row_csv_strip['authors'] = row_csv_strip['authors'].split(';')
        # tag_names
        row_csv_strip['tag_names'] = row_csv_strip['tag_names'].split(';')
        # dictデータを１行追加
        csv_data.append(row_csv_strip)
    
    # １行ずつ、bookへ追加 または編集する
    for d in csv_data:
        set_registered_book_data(d)

    return None


def regist_publisher_csv():
    """ publisherのcsvを登録
    """
    f = request.files['csv_file']
    filename = secure_filename(f.filename)
    ext = Path(filename).suffix
    if ext != '.csv':
        return v_maintenance.main()

    # CSVファイルを読み込む
    row_index = -1
    csv_data = []
    csv_columns = ['publisher_code','publisher_name']
    for l in f:
        row_index += 1
        if row_index==0:
            # １行目はヘッダ
            continue

        row_csv = l.split(',')
        if len(row_csv) != len(csv_columns):
            continue
        row_csv_strip = {}
        for i, col in enumerate(row_csv):
            row_csv_strip[csv_columns[i]] = strip_double_quote(col)
        # dictデータを１行追加
        csv_data.append(row_csv_strip)
    
    # １行ずつ、Publisherへ追加 または編集する
    for d in csv_data:
        set_registered_pub_data(d)

    return None


def strip_double_quote(base_str):
    """ strip_double_quote
    ダブルクォーテーションがあったら削除
    """
    str_ret = base_str

    str_ret = str_ret.strip()
    if (str_ret[0]=='"') and (str_ret[-1]=='"'):
        str_ret = str_ret[1:-1]

    return str_ret


def set_registered_book_data(d):
    """ set_registered_book_data
    CSVで登録された本情報をDBへ登録する
    """
    # publisherがあると登録できないので消しておく
    if 'publisher' in d:
        del d['publisher']

    regist_book(d)

    return None

def set_registered_pub_data(d):
    """ set_registered_pub_data
    CSVで登録された出版者情報をDBへ登録する
    """
    # DBは、pub_codeとpub_nameなので、
    # フルスペルで入っていたら変換しておく
    if 'publisher_code' in d:
        d['pub_code'] = d.pop('publisher_code')
    if 'publisher_name' in d:
        d['pub_name'] = d.pop('publisher_name')

    regist_publisher(d)

    return None
