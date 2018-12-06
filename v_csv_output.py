# -*- coding: utf-8 -*-
""" v_csv_output
DataStoreのデータをCSV出力
"""
from flask import Flask, render_template, request, send_file
from pathlib import Path
import datetime
import zipfile
from io import StringIO, BytesIO
import csv

from models import get_books_by_str, get_publishers, get_tags

#　ダウンロード用のファイルを準備するフォルダ
WORK_DIR = './work'


def main():
    """main
    """
    # ダウンロード用のファイルを作成
    file_path = Path('%s/files.zip' % WORK_DIR)

    data = create_zip(file_path)
    return send_file(data, attachment_filename='books_data.zip', as_attachment=True)


def create_zip(zip_file_path):
    """ create_zip
    複数のcsvをzip圧縮した、zipファイルを作成する。

    Args:
        zip_file_path (str): 作成するzipファイルのパス
    
    Returns:
        (BytesIO): zipデータ
    
    参考:
        https://stackoverflow.com/questions/27337013/how-to-send-zip-files-in-the-python-flask-framework
    """
    dt_now = datetime.datetime.now()

    # CSVを作成する
    files = create_csvs()
    
    # zip圧縮する
    mem_zip = BytesIO()
    with zipfile.ZipFile(mem_zip, 'w') as zf:
        for individualFile in files:
            data = zipfile.ZipInfo(individualFile['file_name'])
            data.date_time = (dt_now.year, dt_now.month, dt_now.day, dt_now.hour, dt_now.minute, dt_now.second)
            data.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(data, individualFile['file_data'])
    mem_zip.seek(0)
    return mem_zip
    

def create_csvs():
    """ create_csvs
    保存するcsvファイルを作成する

    Returns:
        (list(dict)): 作成したCSVファイルのリスト
                      dict file_name(str): ファイル名
                           file_data(BytesIO): ファイルデータ
    
    参考:
        https://qiita.com/hirohuntexp/items/3a1bf3f195a50424c211
    """
    # 今の時間を取得して、ファイルのサフィックスに使用する
    dt_now = datetime.datetime.now()
    str_now = dt_now.strftime('%Y%m%d_%H%M%S')

    ret_csvs = []

    # Book
    with BytesIO() as data_book:
        writer_book = csv.writer(data_book, quotechar='"', quoting=csv.QUOTE_ALL, lineterminator="\n")
        writer_book.writerow([u'title',u'publisher',u'authors',u'comment',u'tags',u'isbn',u'image_url'])
        bs = get_books_by_str()
        for b in bs:
            # authors
            authors = u''
            for a in b['authors']:
                if len(authors)>0:
                    authors += u';'
                authors += a
            # tags
            tags = u''
            for tag in b['tags']:
                if len(tags)>0:
                    tags += u';'
                tags += tag
            print(tags.encode('utf-8'))
            # 出力
            writer_book.writerow([
                b['title'].encode('utf-8'),
                b['publisher'].encode('utf-8'),
                authors.encode('utf-8'),
                b['comment'].encode('utf-8'),
                tags.encode('utf-8'),
                b['isbn'].encode('utf-8'),
                b['image_url'].encode('utf-8')
            ])
        ret_csvs.append({'file_name':'book.csv', 'file_data':data_book.getvalue()})
    
    # Publisher
    with BytesIO() as data_pub:
        writer_pub = csv.writer(data_pub, quotechar='"', quoting=csv.QUOTE_ALL, lineterminator="\n")
        writer_pub.writerow([u'publisher_code',u'publisher_name'])
        ps = get_publishers()
        for p in ps:
            # 出力
            writer_pub.writerow([
                p['pub_code'].encode('utf-8'),
                p['pub_name'].encode('utf-8')
            ])
        ret_csvs.append({'file_name':'publisher.csv', 'file_data':data_pub.getvalue()})

    # Tag
    with BytesIO() as data_tag:
        writer_tag = csv.writer(data_tag, quotechar='"', quoting=csv.QUOTE_ALL, lineterminator="\n")
        writer_tag.writerow([u'tag_name'])
        ts = get_tags()
        for t in ts:
            # 出力
            writer_tag.writerow([
                t['tag_name'].encode('utf-8'),
            ])
        ret_csvs.append({'file_name':'tag.csv', 'file_data':data_tag.getvalue()})

    return ret_csvs

