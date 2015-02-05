# twingo

## お知らせ

当プロジェクトは更新を終了しました。今後は後継プロジェクトの [twingo2](https://github.com/7pairs/twingo2) をよろしくお願いいたします。

## 概要

"twingo" は、TwitterのOAuthを利用したDjangoの認証バックエンドです。
Twitterのユーザー情報を利用したログインの仕組みを、簡単な記述でアプリケーションに組み込むことができます。

## バージョン

Python2.7 + Django1.4での動作を確認しております。

## インストール

同梱の `setup.py` を実行してください。

```
python setup.py install
```

pipを利用して、GitHubから直接インストールすることもできます。

```
pip install git+https://github.com/7pairs/twingo.git
```

## 設定

twingoをDjangoから呼び出すための設定を行います。
`settings.py` の `INSTALLED_APPS` に `twingo` の記述を追加してください。

```
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'yourproject.yourapplication',
    'twingo',  # ←追加
)
```

さらに、twingoを認証バックエンドとするための設定を行います。
同じく `settings.py` に以下の記述を追加してください。

```
AUTHENTICATION_BACKENDS = (
    'twingo.backends.TwitterBackend',
)
```

また、あわせて `settings.py` に以下の定数を定義してください。

* `CONSUMER_KEY` : Twitter APIのConsumer Key。
* `CONSUMER_SECRET` : Twitter APIのConsumer Secret。

なお、以下の定数を定義することで、twingoのデフォルトの動作を変更することができます（任意）。

* `AFTER_LOGIN_URL` : ログイン成功後のリダイレクト先URL。デフォルトは `/` 。
* `AFTER_LOGOUT_URL` : ログアウト後のリダイレクト先URL。デフォルトは `/` 。

## URLディスパッチャー

最後に、`urls.py` に以下の設定を追加してください。

```
urlpatterns = patterns('',
    # 中略
    url(r'^authentication_url/', include('twingo.urls'))  # ←追加
)
```

第1引数の `r'^authentication_url/` は任意のURLで構いません。その配下のURLでtwingoが動作します。

## ユーザープロファイル

twingoはDjangoのユーザープロファイルに対応しています。
twingoの情報をユーザープロファイルとして使用する場合、 `settings.py` に以下の記述を追加してください。

```
AUTH_PROFILE_MODULE = 'twingo.profile'
```
