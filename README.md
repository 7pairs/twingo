# twingo

## はじめに

"Twingo"とは、TwitterのOAuthを利用したDjango用の認証バックエンドです。
あなたのアプリケーションに、Twitterのユーザー情報を利用したログインの仕組みを組み込むことができます。

## 導入準備

TwingoはDjango用の認証バックエンドですので、当然のことながらDjangoが必要になります。
pipなどでインストールしておいてください。

また、Twitterへのアクセスの際にTweepyを使用しています。
こちらも別途インストールしておいてください。

## 設定

まずは、Twingoのファイル一式をあなたのアプリケーションから参照できるパスに配置してください。

続いて、あなたのアプリケーションからTwingoを呼び出す設定をします。
settings.pyのINSTALLED_APPSに"twingo"の記述を追加してください。

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

さらに、Twingoを認証バックエンドとする設定を行います。
settings.pyに以下のように記述してください。

```
AUTHENTICATION_BACKENDS = (
    'twingo.backends.TwitterBackend',
)
```

また、併せてsettings.pyに以下の定数を定義してください。

* CONSUMER_KEY : あなたのアプリケーションのConsumer Key。
* CONSUMER_SECRET : あなたのアプリケーションのConsumer Secret。

なお、任意で以下の定数を定義することで、Twingoのデフォルトの動作を変更することもできます。

* CALLBACK_URL : Twitterからのコールバック時に呼び出されるURL。デフォルトは"http://(HTTP_HOST)/callback/"。
* TOP_URL : あなたのサイトのトップ画面のURL。デフォルトは "/" 。

## URLディスパッチャー

最後に、あなたのアプリケーションのurls.pyに以下の設定を追加してください。

* ログインURLへのアクセス時 : "twingo.views.twitter_login"
* TwitterからのコールバックURLへのアクセス時 : "twingo.views.twitter_callback"
* ログアウトURLへのアクセス時 : "twingo.views.twitter_logout"

例えば、以下のような記述内容になります。

```
urlpatterns = patterns('',
    url(r'^accounts/login/$', 'twingo.views.twitter_login', name='login'),
    url(r'^callback/$', 'twingo.views.twitter_callback', name='callback'),
    url(r'^accounts/logout/$', 'twingo.views.twitter_logout', name='logout'),
)
```

## ユーザープロファイル

TwingoはDjangoのユーザープロファイルに対応しています。
Twingoの情報をユーザープロファイルとして使用したい場合、settings.pyに以下の記述を追加してください。

```
AUTH_PROFILE_MODULE = 'twingo.profile'
```

