# -*- coding: utf-8 -*-

from google.appengine.ext import ndb

from .clsTag import Tag

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

