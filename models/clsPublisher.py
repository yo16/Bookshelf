# -*- coding: utf-8 -*-

from google.appengine.ext import ndb


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

