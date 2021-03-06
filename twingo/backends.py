# -*- coding: utf-8 -*-

#
# Copyright 2015-2019 Jun-ya HASEBA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from tweepy import API, OAuthHandler
from tweepy.error import TweepError

from django.conf import settings
from django.contrib.auth.models import User

from twingo.models import Profile


class TwitterBackend:
    """
    TwitterのOAuthを利用した認証バックエンド。
    ModelBackendの代替として使用することを想定している。
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

        # Profile/Userを取得/作成する
        try:
            profile = Profile.objects.get(twitter_id=twitter_user.id)
            user = profile.user
        except Profile.DoesNotExist:
            # Userを作成する
            user = User()
            user.username = twitter_user.id
            user.first_name = twitter_user.screen_name
            user.last_name = twitter_user.name
            user.set_unusable_password()
            user.save()

            # Profileを作成する
            profile = Profile()
            profile.twitter_id = twitter_user.id
            profile.screen_name = twitter_user.screen_name
            profile.name = twitter_user.name
            profile.description = twitter_user.description
            profile.url = twitter_user.url
            profile.profile_image_url = twitter_user.profile_image_url
            profile.user = user
            profile.save()

        # 有効なユーザーであるかチェックする
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
