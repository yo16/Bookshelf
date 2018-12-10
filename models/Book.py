# -*- coding: utf-8 -*-

from google.appengine.ext import ndb

from .Tag import regist_tag, get_tag_by_id
from .Publisher import get_publisher_by_id, slice_publisher_code, \
                       get_publisher_by_pub_code, regist_publisher


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
            print('tag:', tag_name)
            cur_key_id = regist_tag(tag_name)
            book_info['tags'].append(cur_key_id)

        # tag_namesは、キーごと削除
        del book_info['tag_names']

    # publisher_key_idがない場合は、isbnからpublisher_codeを得て、publisher_key_idを作る
    if 'publisher_key_id' not in book_info:
        # key_idがない場合は、isbnから作り出す
        # pub_codeとかpub_nameとかは使わない
        pub_code = slice_publisher_code(book_info['isbn'])
        p = get_publisher_by_pub_code(pub_code)
        if p is None:
            # 見つからなかったら新規登録
            dict_pub = {
                'pub_code': pub_code,
                'pub_name': '[code]' + pub_code
            }
            book_info['publisher_key_id'] = regist_publisher(dict_pub)
        else:
            # 見つかった場合はそのまま登録
            book_info['publisher_key_id'] = p['key_id']
    
    # publisherがあったら消しておく
    if 'publisher' in book_info:
        del book_info['publisher']
    
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
        """
        # publisher_key_idがない場合は、isbnからpublisher_codeを得る
        if 'publisher_key_id' in book_info:
            print('aaaaa')
            b.publisher_key_id = book_info['publisher_key_id']
        else:
            print('bbbbb')
            # key_idがない場合は、isbnから作り出す
            # pub_codeとかpub_nameとかは使わない
            pub_code = slice_publisher_code(book_info['isbn'])
            p = get_publisher_by_pub_code(pub_code)
            if p is None:
                print('cccccc')
                # 見つからなかったら新規登録
                dict_pub = {
                    'pub_code': pub_code,
                    'pub_name': '[code]' + pub_code
                }
                b.publisher_key_id = regist_publisher(dict_pub)
            else:
                print('ddddd')
                # 見つかった場合はそのまま登録
                b.publisher_key_id = p['key_id']
        """

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
    Bookが検索条件にあうかどうかを判断する。
    大文字小文字を区別せず検索するために、全て小文字に変換して検索する。

    Args:
        b (Book): 調査対象のBookインスタンス
        list_s (list(str)): 検索文字列のリスト

    Returns:
        True: マッチ
        False: アンマッチ
    """
    # list_sのどれか１つでもマッチしたらTrue（or検索）
    for s in list_s:
        s_l = s.lower()
        
        # タイトルまたはコメント
        title_l = b.title.lower()
        comment_l = b.comment.lower()
        if (s_l in title_l) or (s_l in comment_l):
            return True
    
        # 著者
        for a in b.authors:
            a_l = a.lower()
            if s_l in a_l:
                return True
    
        # タグ
        for t in b.tags:
            tag_info = get_tag_by_id(t)
            tag_name_l = tag_info['tag_name'].lower()
            if s_l in tag_name_l:
                return True

    return False


def delete_book(isbn):
    """ delete_book
    isbnをキーにBookを削除する。

    Args:
        isbn (str): 削除する本のISBN
    """
    b = get_book_by_isbn(isbn)
    if b is not None:
        b.key.delete()

    return None
