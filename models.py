# -*- coding: utf-8 -*-
""" Books, Book, Tag, Publisher
2018/11/10 y.ikeda
"""
from google.appengine.ext import ndb


class Books():
    """ Booksクラス
    Datastoreのkindではない。
    Bookの操作用のクラス。
    """
    #_books = []

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
                tag_key = ndb.Key(Tag, t_keyid)
                t = tag_key.get()
                cur_book['tags'].append(t.tag_name)
            bs.append(cur_book)

        return bs, cur_page, last_page


class Book(ndb.Model):
    """ Book Model class
    kind['Book'] - entity
    """
    title = ndb.StringProperty()
    authors = ndb.StringProperty(repeated=True)
    publisher_key_id = ndb.IntegerProperty()
    isbn = ndb.StringProperty()
    image_url = ndb.StringProperty()
    comment = ndb.StringProperty()
    tags = ndb.IntegerProperty(repeated=True)


    @staticmethod
    def regist_book(book_info):
        """ regist_book
        Bookへ登録する。ISBNがすでに登録されている場合は上書きする。

        Args:
            book_info (dict): Bookのプロパティをキーに持つdict。
        
        Returns:
            (int): 登録、または更新されたBookのkey_id
        """
        # Tagにtag_nameをキーに問い合わせて、無かったら登録。
        # そのTagのkey_idをbook_info['tags']に入れる。
        book_info['tags'] = []
        if 'tag_names' in book_info:
            for tag_name in book_info['tag_names']:
                # 登録 or 更新
                tag_key = Tag.regist_tag(tag_name)
                
                #print('t.id:', tag_key.integer_id())
                cur_key_id = tag_key.integer_id()
                book_info['tags'].append(cur_key_id)

            # tag_namesは、キーごと削除
            del book_info['tag_names']

        # Bookにisbnをキーに問い合わせて、無かったら登録
        b = Book.query(Book.isbn==book_info['isbn']).get()
        if b is None:
            # 登録
            Book(**book_info).put()
        else:
            # あったら更新
            b.title = book_info['title']
            b.authors = []
            for a in book_info['authors']:
                b.authors.append(a)
            b.publisher_key_id = book_info['publisher_key_id']
            b.image_url = book_info['image_url']
            b.comment = book_info['comment']
            b.tags = []
            for t in book_info['tags']:
                b.tags.append(t)

            #for k, v in book_info.items():
            #    setattr(b, k, v)
            #    #b[k] = v
            b.put()

    @staticmethod
    def get_book_by_isbn(isbn):
        b_key = Book.query(Book.isbn==isbn)
        if b_key is None:
            return None
        return b_key.get()


class Publisher(ndb.Model):
    """ Publisher Model class
    kind['Publisher'] - entity
    """
    pub_code = ndb.StringProperty()
    pub_name = ndb.StringProperty()

    @staticmethod
    def get_publisher_by_id(key_id):
        """get_publisher_by_id
        DatastoreのキーIDから、Publisherを得る

        Args:
            key_id (str): Publisherのkey_id
        
        Returns:
            (str): 出版者名
        """
        p_key = ndb.Key(Publisher, key_id)
        if p_key is None:
            return None
        
        return p_key.get()
    

    @staticmethod
    def get_publisher_by_pub_code(publisher_code):
        """get_publisher_by_pub_code
        出版者コードから、Publisherを得る

        Args:
            publisher_code (str): 出版者コード
        
        Returns:
            (Publisher):　Publisherオブジェクト
        """
        return xx


class Tag(ndb.Model):
    """ Tag Model class
    kind['Tag'] - entity
    """
    tag_name = ndb.StringProperty()

    @staticmethod
    def regist_tag(tag_name_):
        """タグを登録または更新する
        
        Args:
            tag_name_ (str): タグの文字列
        
        Returns:
            (int): 登録 or 更新されたTagのkey_id
        """
        t = Tag.query(Tag.tag_name==tag_name_).get()
        tag_key = None
        if t is None:
            # 登録
            reg_tag = {'tag_name': tag_name_}
            tag_key = Tag(**reg_tag).put()
        else:
            # あったらキーを返す
            tag_key = t.key
        
        return tag_key
    

    @staticmethod
    def get_tag_by_id(key_id):
        """get_tag_by_id
        DatastoreのキーIDから、Tagを得る

        Args:
            key_id (str): Tagのkey_id
        
        Returns:
            (str): タグ名
        """
        t_key = ndb.Key(Tag, key_id)
        if t_key is None:
            return None
        
        return t_key.get()
    