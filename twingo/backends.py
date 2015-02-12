# -*- coding: utf-8 -*-

from tweepy import API, OAuthHandler
from tweepy.error import TweepError

from django.conf import settings
from django.contrib.auth.models import User

from twingo.models import Profile


class TwitterBackend:
    """
    TwitterのOAuthを利用した認証バックエンド。
    ModelBackendの代替として設定することを想定している。
    """

    def authenticate(self, access_token):
        """
        Twitterから取得したアクセストークンをもとに認証を行う。

        :param access_token: アクセストークン
        :type access_token: tuple
        :return: ユーザー情報
        :rtype: django.contrib.auth.models.User
        """
        # APIオブジェクトを構築する
        oauth_handler = OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
        oauth_handler.set_access_token(access_token[0], access_token[1])
        api = API(oauth_handler)

        # ログインユーザーのTwitter情報を取得する
        try:
            twitter_user = api.me()
        except TweepError:
            return None

        # ProfileとUserを取得する
        try:
            profile = Profile.objects.get(twitter_id=twitter_user.id)
            user = profile.user
        except Profile.DoesNotExist:
            # Userを新規作成する
            user = User()
            user.username = twitter_user.id
            user.first_name = twitter_user.screen_name
            user.last_name = twitter_user.name
            user.password = 'Ruquia is my wife.'
            user.save()

            # Profileを新規作成する
            profile = Profile()
            profile.twitter_id = twitter_user.id
            profile.name = twitter_user.name
            profile.screen_name = twitter_user.screen_name
            profile.description = twitter_user.description
            profile.profile_image_url = twitter_user.profile_image_url
            profile.url = twitter_user.url
            profile.user = user
            profile.save()

        # ユーザーが有効であるかチェックする
        if user.is_active:
            return user
        else:
            return None

    def get_user(self, user_id):
        """
        指定されたIDのユーザー情報を取得する。

        :param user_id: UserのID
        :type user_id: int
        :return: ユーザー情報
        :rtype: django.contrib.auth.models.User
        """
        # ユーザー情報を取得する
        try:
            user = User.objects.get(pk=user_id, is_active=True)
            return user
        except User.DoesNotExist:
            return None
