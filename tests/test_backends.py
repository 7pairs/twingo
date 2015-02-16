# -*- coding: utf-8 -*-

#
# Copyright 2015 Jun-ya HASEBA
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

from nose.tools import *
from mock import patch

import factory
from tweepy.error import TweepError

from django.contrib.auth.models import User
from django.test import TestCase

from twingo.backends import TwitterBackend
from twingo.models import Profile


class TwitterUser:
    """
    Twitterのユーザー情報を格納するテスト用クラス。
    """

    def __init__(self, **kwargs):
        """
        TwitterUserを構築する。

        :param kwargs: 設定するプロパティとその値
        :type kwargs: dict
        """
        # プロパティを設定する
        for k, v in kwargs.items():
            setattr(self, k, v)


class UserFactory(factory.DjangoModelFactory):
    """
    Userモデルを作成するファクトリー。
    """
    FACTORY_FOR = User
    username = factory.Sequence(lambda x: 'username_%02d' % x)
    first_name = factory.Sequence(lambda x: 'first_name_%02d' % x)
    last_name = factory.Sequence(lambda x: 'last_name_%02d' % x)
    email = factory.Sequence(lambda x: 'user%02d' % x)
    password = factory.Sequence(lambda x: 'password%02d' % x)
    is_staff = False
    is_active = True
    is_superuser = False


class ProfileFactory(factory.DjangoModelFactory):
    """
    Profileモデルを作成するファクトリー。
    """
    FACTORY_FOR = Profile
    twitter_id = factory.Sequence(lambda x: x)
    name = factory.Sequence(lambda x: 'name_%02d' % x)
    screen_name = factory.Sequence(lambda x: 'screen_name_%02d' % x)
    description = factory.Sequence(lambda x: 'description_%02d' % x)
    profile_image_url = factory.Sequence(lambda x: 'http://dummy.com/%02d.jpg')
    url = factory.Sequence(lambda x: 'http://dummy.com/%02d.html')
    user = factory.LazyAttribute(lambda x: UserFactory())


class DisableUserFactory(UserFactory):
    """
    無効なユーザーのUserモデルを作成するファクトリー。
    """
    is_active = False


class DisableProfileFactory(ProfileFactory):
    """
    無効なユーザーのProfileモデルを作成するファクトリー。
    """
    user = factory.LazyAttribute(lambda x: DisableUserFactory())


class BackendsTest(TestCase):
    """
    backends.pyに対するテストコード。
    """

    @patch('twingo.backends.API')
    @patch('twingo.backends.OAuthHandler')
    def test_authenticate_01(self, oauth_handler, api):
        """
        [対象] TwitterBackend.authenticate()
        [条件] 新規ユーザーでログインする。
        [結果] ユーザーの情報がデータベースに登録され、該当ユーザーのUserオブジェクトが返される。
        """
        api.return_value.me.return_value = TwitterUser(
            id=1402804142,
            screen_name='7pairs',
            name='Jun-ya HASEBA',
            description='This video has been deleted.',
            profile_image_url='https://pbs.twimg.com/profile_images/1402804142/icon_400x400.jpg',
            url='http://seven-pairs.hatenablog.jp/'
        )

        twitter_backend = TwitterBackend()
        actual = twitter_backend.authenticate(('key', 'secret'))

        profile = Profile.objects.get(twitter_id=1402804142)
        assert_equal('Jun-ya HASEBA', profile.name)
        assert_equal('7pairs', profile.screen_name)
        assert_equal('This video has been deleted.', profile.description)
        assert_equal('https://pbs.twimg.com/profile_images/1402804142/icon_400x400.jpg', profile.profile_image_url)
        assert_equal('http://seven-pairs.hatenablog.jp/', profile.url)
        assert_equal('1402804142', profile.user.username)
        assert_equal('7pairs', profile.user.first_name)
        assert_equal('Jun-ya HASEBA', profile.user.last_name)
        assert_equal('Ruquia is my wife.', profile.user.password)
        assert_equal(profile.user, actual)

    @patch('twingo.backends.API')
    @patch('twingo.backends.OAuthHandler')
    def test_authenticate_02(self, oauth_handler, api):
        """
        [対象] TwitterBackend.authenticate()
        [条件] 既存ユーザーでログインする。
        [結果] 該当ユーザーのUserオブジェクトが返される。
        """
        profile = ProfileFactory()
        api.return_value.me.return_value = TwitterUser(id=profile.twitter_id)

        twitter_backend = TwitterBackend()
        actual = twitter_backend.authenticate(('key', 'secret'))

        assert_equal(profile.user, actual)

    @patch('twingo.backends.API')
    @patch('twingo.backends.OAuthHandler')
    def test_authenticate_03(self, oauth_handler, api):
        """
        [対象] TwitterBackend.authenticate()
        [条件] 無効なユーザーでログインする。
        [結果] Noneが返される。
        """
        profile = DisableProfileFactory()
        api.return_value.me.return_value = TwitterUser(id=profile.twitter_id)

        twitter_backend = TwitterBackend()
        actual = twitter_backend.authenticate(('key', 'secret'))

        assert_equal(None, actual)

    @patch('twingo.backends.API')
    @patch('twingo.backends.OAuthHandler')
    def test_authenticate_04(self, oauth_handler, api):
        """
        [対象] TwitterBackend.authenticate()
        [条件] Twitterからエラーが返る。
        [結果] Noneが返される。
        """
        api.return_value.me.side_effect = TweepError('reason')

        twitter_backend = TwitterBackend()
        actual = twitter_backend.authenticate(('key', 'secret'))

        assert_equal(None, actual)

    def test_get_user_01(self):
        """
        [対象] TwitterBackend.get_user()
        [条件] 存在するユーザーのIDを指定する。
        [結果] 該当ユーザーのUserオブジェクトが返される。
        """
        profile = ProfileFactory()

        twitter_backend = TwitterBackend()
        actual = twitter_backend.get_user(profile.user.id)

        assert_equal(profile.user, actual)

    def test_get_user_02(self):
        """
        [対象] TwitterBackend.get_user()
        [条件] 存在しないユーザーのIDを指定する。
        [結果] Noneが返される。
        """
        profile = ProfileFactory()

        twitter_backend = TwitterBackend()
        actual = twitter_backend.get_user(profile.user.id + 1)

        assert_equal(None, actual)

    def test_get_user_03(self):
        """
        [対象] TwitterBackend.get_user()
        [条件] 無効なユーザーのIDを指定する。
        [結果] Noneが返される。
        """
        profile = DisableProfileFactory()

        twitter_backend = TwitterBackend()
        actual = twitter_backend.get_user(profile.user.id)

        assert_equal(None, actual)
