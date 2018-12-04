# -*- coding: utf-8 -*-
""" v_csv_output
DataStoreのデータをCSV出力
"""
from flask import Flask, render_template, request, send_file
from pathlib import Path
import datetime
import zipfile

from models import get_books_by_str

#　ダウンロード用のファイルを準備するフォルダ
WORK_DIR = './work'


def main():
    """main
    """
    # ダウンロード用のファイルを作成
    file_path = Path('%s/files.zip' % WORK_DIR)

    create_zip(file_path)

    return send_file(
        file_path,
        mimetype='application/zip', 
        attachment_filename=file_path.name, 
        as_attachment=True)


def create_zip(zip_file_path):
    """ create_zip
    複数のcsvをzip圧縮した、zipファイルを作成する。

    Args:
        zip_file_path (str): 作成するzipファイルのパス
    """
    # CSVを作成する
    files = create_csvs()

    # zip圧縮する
    with zipfile.ZipFile(zip_file_path, 'w', compression=zipfile.ZIP_DEFLATED) as new_zip:
        for f in files:
            p = Path(f)
            new_zip.write(f, arcname=p)

    return    
    

def create_csvs():
    """ create_csvs
    保存するcsvファイルを作成する

    Returns:
        (list(str)): 作成したCSVファイルパスのリスト
    """
    # 今の時間を取得して、ファイルのサフィックスに使用する
    dt_now = datetime.datetime.now()
    str_now = dt_now.strftime('%Y%m%d_%H%M%S')

    ret_csv = []

    # Book
    csv_book_path = '%s/Book_%s.csv' % (WORK_DIR, str_now)
    with open(csv_book_path, mode='w') as f:    # ＊＊＊ ここでエラーになる ＊＊＊
                                                # GAEではローカルに保存できない！！
        f.write('title,publisher,authors,comment,tags,isbn,image_url')
        bs = get_books_by_str()
        for b in bs:
            # publisher_name
            publisher_name = get_publisher_by_id(b.publisher)['publisher_name']
            # authors
            authors = ''
            for a in b.authors:
                if len(authors)>0:
                    authors += ';'
                authors += a
            # tags
            tags = ''
            for tag_key in b.tags:
                t = get_tag_by_id(tag_key)
                if len(tags)>0:
                    tags += ';'
                tags += t['tag_name']
            # 出力
            f.write('%s,%s,%s,%s,%s,%s,%s' % 
                (b.title, publisher_name, authors,
                 b.comment, tags, b.isbn, b.image_url)
            )
    csv_book_path.append(csv_book_path)
    
    return csv_book_path

