# -*- coding: utf-8 -*-

"""
Twingoで利用する認証バックエンドを提供します。

@author: Jun-ya HASEBA
"""

from django.conf import settings
from django.contrib.auth.models import User

import tweepy

from twingo.models import Profile


class TwitterBackend:
    """
    TwitterのOAuthを利用した認証バックエンドです。
    ModelBackendの代替として使用してください。
    """

    def authenticate(self, access_token):
        """
        Twitterから取得したアクセストークンをもとに認証を行います。

        @param access_token: Twitterから取得したアクセストークン
        @type access_token: str
        @return: 認証成功時はユーザーの情報を格納したUser。
                 認証失敗時はNone。
        @rtype: django.contrib.auth.models.User
        """
        # APIオブジェクトを構築
        oauth_handler = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
        oauth_handler.set_access_token(access_token.key, access_token.secret)
        api = tweepy.API(oauth_handler)

        # ログインしようとしているユーザーのTwitter情報を取得
        try:
            twitter_user = api.me()
        except:
            return None

        # ProfileとUserを取得
        try:
            profile = Profile.objects.get(twitter_id=twitter_user.id)
            user = profile.user
        except Profile.DoesNotExist:
            # Userを新規作成
            user = User()
            user.username = twitter_user.id
            user.first_name = twitter_user.screen_name
            user.last_name = twitter_user.name
            user.password = 'Ruquia is my wife.'  # ルキアは俺の嫁
            user.save()

            # Profileを新規作成
            profile = Profile()
            profile.twitter_id = twitter_user.id
            profile.name = twitter_user.name
            profile.screen_name = twitter_user.screen_name
            profile.description = twitter_user.description
            profile.profile_image_url = twitter_user.profile_image_url
            profile.url = twitter_user.url
            profile.user = user
            profile.save()

        # 認証済みのUserを返す
        if user.is_active:
            return user
        else:
            return None

    def get_user(self, user_id):
        """
        指定されたIDのUserを取得します。

        @param user_id: Userのプライマリーキー
        @type user_id: int
        @return: 取得したUser。
                 取得できなかった場合はNone。
        @rtype: django.contrib.auth.models.User
        """
        # Userを取得
        try:
            user = User.objects.get(pk=user_id, is_active=True)
            return user
        except User.DoesNotExist:
            return None

