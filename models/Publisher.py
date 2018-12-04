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
    pub_key = Publisher(**publisher_info).put()
    return pub_key.integer_id()

