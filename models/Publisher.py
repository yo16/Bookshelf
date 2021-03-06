# -*- coding: utf-8 -*-

from google.appengine.ext import ndb


class Publisher(ndb.Model):
    """ Publisher Model class
    kind['Publisher'] - entity
    """
    pub_code = ndb.StringProperty()
    pub_name = ndb.StringProperty()


def get_publisher_by_id(key_id):
    """get_publisher_by_id
    DatastoreのキーIDから、Publisherを得る

    Args:
        key_id (str): Publisherのkey_id
    
    Returns:
        (dict): 出版者情報
    """
    p_key = ndb.Key(Publisher, key_id)
    if p_key is None:
        return None
    p = p_key.get()

    pub_info = {
        'key_id': p.key.integer_id(),
        'pub_name': p.pub_name,
        'pub_code': p.pub_code
    }
    return pub_info


def get_publisher_by_pub_code(publisher_code):
    """get_publisher_by_pub_code
    出版者コードから、Publisherを得る

    Args:
        publisher_code (str): 出版者コード
    
    Returns:
        (dict):　出版者情報
    """
    pub_info = None

    q = Publisher.query(Publisher.pub_code == publisher_code).get()
    if q is not None:
        pub_name = q.pub_name
        pub_id = q.key.integer_id()

        pub_info = {
            'key_id': q.key.integer_id(),
            'pub_name': q.pub_name,
            'pub_code': q.pub_code
        }

    return pub_info


def regist_publisher(publisher_info):
    """ regist_publisher
    Publisher情報から、Publisherへ登録する

    Args:
        publisher_info (dict): 出版者情報
    
    Returns:
        (int): 登録されたBookのkey_id
    """
    # PublisherにPubCodeを問い合わせて、無かったら登録
    p = Publisher.query(
            Publisher.pub_code==publisher_info['pub_code']
        ).get()
    pub_key = 0
    if p is None:
        # 登録
        pub_key = Publisher(**publisher_info).put()
    else:
        # あったら更新
        p.pub_name = publisher_info['pub_name']
        p.put()
        # 更新したキー
        pub_key = p.key
    
    return pub_key.integer_id()


def get_publishers():
    """ get_publishers
    登録されている出版者情報を返す

    Args:
        None
    
    Returns:
        (list(dict)): 出版者情報
    """
    q = Publisher.query()
    pub_db = q.fetch()

    ret_pubs = []
    for p in pub_db:
        cur_pub = {}
        cur_pub['pub_name'] = p.pub_name
        cur_pub['pub_code'] = p.pub_code

        ret_pubs.append(cur_pub)
    
    return ret_pubs


def slice_publisher_code(isbn):
    """ 出版社コードを抜き出して返す
    """
    top2 = int(isbn[4:6])
    keta = 2
    if top2 < 20:
        keta = 2
    elif top2 < 70:
        keta = 3
    elif top2 < 85:
        keta = 4
    elif top2 < 90:
        keta = 5
    elif top2 < 95:
        keta = 6
    else:
        keta = 7
    return isbn[4:4+keta]
