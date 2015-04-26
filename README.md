# twingo

[![Build Status](https://travis-ci.org/7pairs/twingo.svg?branch=master)](https://travis-ci.org/7pairs/twingo)
[![Coverage Status](https://coveralls.io/repos/7pairs/twingo/badge.svg?branch=master)](https://coveralls.io/r/7pairs/twingo?branch=master)

## 重要なお知らせ

当プロジェクトは更新を終了しました。後継プロジェクトの [twingo2](https://github.com/7pairs/twingo2) をよろしくお願いします。

## 概要

"twingo"は、TwitterのOAuthを利用したDjangoの認証バックエンドです。
Twitterのユーザー情報による認証の仕組みを簡単な記述でアプリケーションに組み込むことができます。

## バージョン

Python2.7 + Django1.4での動作を確認しています。また、Python2.6 + Django1.4の組み合わせでもユニットテストを実施しています。

## インストール

同梱の `setup.py` を実行してください。

```console
$ python setup.py install
```

pipを利用し、GitHubから直接インストールすることもできます。

```console
$ pip install git+https://github.com/7pairs/twingo.git
```

## 設定

twingoをDjangoから呼び出すための設定を行います。
まず、 `settings.py` の `INSTALLED_APPS` に `twingo` を追加してください。

```python
INSTALLED_APPS = (
    # (中略)
    'twingo',  # ←追加
)
```

さらに、twingoを認証バックエンドとするための設定を行います。
同じく `settings.py` に以下の記述を追加してください。

```python
AUTHENTICATION_BACKENDS = (
    'twingo.backends.TwitterBackend',
)
```

また、あわせて `settings.py` に以下の定数を定義してください。

|定数名|設定する値|
|---|---|
|`CONSUMER_KEY`|Twitter APIのConsumer Key|
|`CONSUMER_SECRET`|Twitter APIのConsumer Secret|

なお、以下の定数を定義することでtwingoのデフォルトの動作を上書きすることができます（任意）。

|定数名|設定する値|デフォルト値|
|---|---|---|
|`AFTER_LOGIN_URL`|ログイン成功後のリダイレクト先URL|`/`|
|`AFTER_LOGOUT_URL`|ログアウト後のリダイレクト先URL|`/`|

## URLディスパッチャー

`urls.py` に以下の記述を追加してください。

```python
urlpatterns = patterns('',
    # (中略)
    (r'^authentication_url/', include('twingo.urls'))  # ←追加
)
```

`r'^authentication_url/'` は任意のURLで構いません。その配下のURLでtwingoが動作します。

また、 `@login_required` デコレータを使用する場合、 `settings.py` に以下の記述を追加してください。

```python
LOGIN_URL = 'authentication_url/login/'
```

`authentication_url` の部分は `urls.py` にて設定した値と同一のものにしてください。

## ユーザープロファイル

twingoはDjangoのユーザープロファイルに対応しています。
twingoで保持する情報をユーザープロファイルとして使用する場合、 `settings.py` に以下の記述を追加してください。

```python
AUTH_PROFILE_MODULE = 'twingo.profile'
```

## ライセンス

twingoは [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0) にて提供します。
ただし、twingoが依存している [Tweepy](https://github.com/tweepy/tweepy) は [The MIT License](http://opensource.org/licenses/mit-license.php) により提供されていますのでご注意ください。
