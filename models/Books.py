# -*- coding: utf-8 -*-

from .Book import get_books_by_str


def get_books(search_strs=[], page=0, num_per_page=20):
    """ get_books
    search_strをキーに検索した結果の本dictionaryのリストを返す
    
    Args:
        search_strs (list(str)): 検索キーワードの配列。
        page (int): ページ番号。0から始まる整数。
        num_per_page (int): １ページあたりの件数。
    
    Returns:
        (list): Bookのdictionaryのリスト
        (int): ページ番号。
                不正なページ番号が指示された場合に入力と異なる。
        (int): 最終ページ番号。
    """
    # DBから検索
    bs_db = get_books_by_str(search_strs)
    
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

    return bs_db, cur_page, last_page
