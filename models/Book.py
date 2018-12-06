# -*- coding: utf-8 -*-

from google.appengine.ext import ndb

from .Tag import regist_tag, get_tag_by_id
from .Publisher import get_publisher_by_id


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


def get_books_by_str(search_str=''):
    """ get_books
    Datastoreから検索

    Args:
        search_str (str): 検索する文字列。
                          ''の場合は、条件なし
    
    Returns:
        (list(dict(Book like))): 辞書の配列
    """
    bs_db = None
    if 0<len(search_str):
        # 検索文字列がある場合は検索
        bs_db = search_books(search_str)
    else:
        # ない場合は、全体検索
        q = Book.query()
        bs_db = q.fetch()
    
    # 検索結果をdictに詰め替える
    ret_books = []
    for b in bs_db:
        cur_book = {}
        cur_book['title'] = b.title
        cur_book['authors'] = []
        for a in b.authors:
            cur_book['authors'].append(a)
        pub = get_publisher_by_id(b.publisher_key_id)
        cur_book['publisher'] = pub['pub_name']
        cur_book['isbn'] = b.isbn
        if (b.image_url is None) or (len(b.image_url)==0):
            b.image_url = '/static/img/NoImage.png'
        cur_book['image_url'] = b.image_url
        cur_book['comment'] = b.comment
        cur_book['tags'] = []
        for t_keyid in b.tags:
            t = get_tag_by_id(t_keyid)
            cur_book['tags'].append(t['tag_name'])
        ret_books.append(cur_book)

    return ret_books


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
            cur_key_id = regist_tag(tag_name)
            book_info['tags'].append(cur_key_id)

        # tag_namesは、キーごと削除
        del book_info['tag_names']

    # Bookにisbnをキーに問い合わせて、無かったら登録
    b = Book.query(Book.isbn==book_info['isbn']).get()
    if b is None:
        # 登録
        b_key = Book(**book_info).put()
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
        b.put()
        
        # 更新したキー
        b_key = b.key
    
    return b_key.integer_id()


def get_book_by_isbn(isbn):
    b_key = Book.query(Book.isbn==isbn)
    if b_key is None:
        return None
    return b_key.get()


def search_books(search_strs=[]):
    """ search_books
    タイトル、コメント、著者、タグを検索する
    
    Args:
        search_strs (list(str)): 検索する文字列の配列。
    
    Returns:
        (list): Bookインスタンスの配列
    """
    # とりあえず無条件で検索
    q = Book.query()
    bs_db = q.fetch()

    # １つずつ見て、条件に合うものを探す
    ret_bs = []
    for b in bs_db:
        found = False
        if is_match(b, search_strs):
            ret_bs.append(b)
    
    return ret_bs


def is_match(b, list_s):
    """ is_match
    Bookが検索条件にあうかどうかを判断する

    Args:
        b (Book): 調査対象のBookインスタンス
        list_s (list(str)): 検索文字列のリスト

    Returns:
        True: マッチ
        False: アンマッチ
    """
    # list_sのどれか１つでもマッチしたらTrue（or検索）
    for s in list_s:
        # タイトルまたはコメント
        if (s in b.title) or (s in b.comment):
            return True
    
        # 著者
        for a in b.authors:
            if s in a:
                return True
    
        # タグ
        for t in b.tags:
            tag_info = get_tag_by_id(t)
            if s in tag_info['tag_name']:
                return True

    return False
        