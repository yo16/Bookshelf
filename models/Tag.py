# -*- coding: utf-8 -*-

from google.appengine.ext import ndb


class Tag(ndb.Model):
    """ Tag Model class
    kind['Tag'] - entity
    """
    tag_name = ndb.StringProperty()


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
    
    return tag_key.integer_id()


def get_tag_by_id(key_id):
    """get_tag_by_id
    DatastoreのキーIDから、Tagを得る

    Args:
        key_id (str): Tagのkey_id
    
    Returns:
        (dict): タグ情報
    """
    t_key = ndb.Key(Tag, key_id)
    if t_key is None:
        return None
    t = t_key.get()
    
    tag_info = {
        'key_id': t_key.integer_id(),
        'tag_name': t.tag_name
    }
    
    return tag_info
