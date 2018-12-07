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
from models import regist_book

def main():
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
        set_registered_data(d)

    return v_maintenance.main()


def strip_double_quote(base_str):
    """ strip_double_quote
    ダブルクォーテーションがあったら削除
    """
    str_ret = base_str

    str_ret = str_ret.strip()
    if (str_ret[0]=='"') and (str_ret[-1]=='"'):
        str_ret = str_ret[1:-1]

    return str_ret


def set_registered_data(d):
    """ set_registered_data
    CSVで登録された情報をDBへ登録する
    """
    # publisherがあると登録できないので消しておく
    if 'publisher' in d:
        del d['publisher']

    regist_book(d)

    return None
