# -*- coding: utf-8 -*-

from .clsBook import Book
from .clsPublisher import Publisher
from .clsTag import Tag

class Books():
    """ Booksクラス
    Datastoreのkindではない。
    Bookの操作用のクラス。
    """

    @staticmethod
    def get_books(search_str='', page=0, num_per_page=20):
        """ get_books
        search_strをキーに検索した結果の本dictionaryのリストを返す
        
        Args:
            search_str (str): 検索キーワード。
            page (int): ページ番号。0から始まる整数。
            num_per_page (int): １ページあたりの件数。
        
        Returns:
            (list): Bookのdictionaryのリスト
            (int): ページ番号。
                   不正なページ番号が指示された場合に入力と異なる。
            (int): 最終ページ番号。
        """
        # DBから検索
        if 0<len(search_str):
            # 検索文字列がある場合は検索
            q = Book.query()   # under construction!
            bs_db = q.fetch()   # under construction!
        else:
            # ない場合は、全体検索
            q = Book.query()
            bs_db = q.fetch()
        
        # 指示されたページの要素番号を計算する
        cur_page = page
        last_page = int(len(bs_db) / num_per_page)
        if cur_page<0:
            cur_page = 0
        elif len(bs_db) <= cur_page * num_per_page:
            # データ量を超えたページ指定の場合は最終ページ
            cur_page = last_page
        
        # fetchした結果を、ページングするデータだけに絞る
        start_item = cur_page * num_per_page
        end_item = start_item + num_per_page - 1
        bs_db = bs_db[start_item : end_item+1]

        # dictionaryに詰め替える
        bs = []
        for b in bs_db:
            cur_book = {}
            cur_book['title'] = b.title
            cur_book['authors'] = []
            for a in b.authors:
                cur_book['authors'].append(a)
            pub = Publisher.get_publisher_by_id(b.publisher_key_id)
            cur_book['publisher'] = pub.pub_name
            cur_book['isbn'] = b.isbn
            if (b.image_url is None) or (len(b.image_url)==0):
                b.image_url = '/static/img/NoImage.png'
            cur_book['image_url'] = b.image_url
            cur_book['comment'] = b.comment
            cur_book['tags'] = []
            for t_keyid in b.tags:
                t = Tag.get_tag_by_id(t_keyid)
                cur_book['tags'].append(t.tag_name)
            bs.append(cur_book)

        return bs, cur_page, last_page
