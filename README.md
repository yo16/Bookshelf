# Bookshelf
持っている本を管理する。

## 機能概要
- ISBNコードから本を検索して、登録する。
- 登録された一覧を見ることができる。

## システム概要
- GAE StandardEdition(python2.7)で動作確認。
- HTTPはflask。
- データは、Datastoreに格納。
