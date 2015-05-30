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

from mock import patch

import factory
from tweepy.error import TweepError

from django.contrib.auth.models import User
from django.test import TestCase

from twingo.models import Profile


class TwitterUser:
    """
    Twitterのユーザー情報を格納するテスト用クラス。
    Tweepyを模したモックによる返却値として使用する。
    """

    def __init__(self, **kwargs):
        """
        TwitterUserを構築する。

        :param kwargs: 設定するプロパティ名とその値
        :type kwargs: dict
        """
        # プロパティを設定する
        for k, v in kwargs.items():
            setattr(self, k, v)


class UserFactory(factory.DjangoModelFactory):
    """
    Userのテストデータを作成するファクトリー。
    """

    class Meta:
        model = User

    username = factory.Sequence(lambda x: 'username_%02d' % x)
    first_name = factory.Sequence(lambda x: 'first_name_%02d' % x)
    last_name = factory.Sequence(lambda x: 'last_name_%02d' % x)
    email = factory.Sequence(lambda x: 'user_%02d@dummy.com' % x)
    password = factory.Sequence(lambda x: 'password_%02d' % x)
    is_staff = False
    is_active = True
    is_superuser = False


class ProfileFactory(factory.DjangoModelFactory):
    """
    Profileのテストデータを作成するファクトリー。
    """

    class Meta:
        model = Profile

    twitter_id = factory.Sequence(lambda x: x)
    screen_name = factory.Sequence(lambda x: 'screen_name_%02d' % x)
    name = factory.Sequence(lambda x: 'name_%02d' % x)
    description = factory.Sequence(lambda x: 'description_%02d' % x)
    url = factory.Sequence(lambda x: 'http://dummy.com/user_%02d.html' % x)
    profile_image_url = factory.Sequence(lambda x: 'http://dummy.com/user_%02d.jpg' % x)
    user = factory.LazyAttribute(lambda x: UserFactory())


class DisableUserFactory(UserFactory):
    """
    無効なユーザーを表すUserのテストデータを作成するファクトリー。
    """

    is_active = False


class DisableProfileFactory(ProfileFactory):
    """
    無効なユーザーを表すProfileのテストデータを作成するファクトリー。
    """

    user = factory.LazyAttribute(lambda x: DisableUserFactory())


class BackendsTest(TestCase):
    """
    backends.pyに対するテストコード。
    """

    def _get_target_object(self):
        """
        テスト対象のオブジェクトを取得する。

        :return: テスト対象のバックエンドオブジェクト
        :rtype: twingo.backends.TwitterBackend
        """
        # テスト対象のオブジェクトを生成する
        from twingo.backends import TwitterBackend
        return TwitterBackend()

    @patch('twingo.backends.API')
    @patch('twingo.backends.OAuthHandler')
    def test_authenticate_01(self, oauth_handler, api):
        """
        [対象] authenticate() : No.01
        [条件] 新規ユーザーでログインする。
        [結果] ユーザーの情報がデータベースに保存され、該当ユーザーのUserオブジェクトが返却される。
        """
        api.return_value.me.return_value = TwitterUser(
            id=1402804142,
            screen_name='7pairs',
            name='Jun-ya HASEBA',
            description='This video has been deleted.',
            url='http://seven-pairs.hatenablog.jp/',
            profile_image_url='https://pbs.twimg.com/profile_images/1402804142/icon_400x400.jpg'
        )

        target = self._get_target_object()
        actual = target.authenticate(('key', 'secret'))

        profile = Profile.objects.get(twitter_id=1402804142)
        self.assertEqual(profile.user, actual)
        self.assertEqual('7pairs', profile.screen_name)
        self.assertEqual('Jun-ya HASEBA', profile.name)
        self.assertEqual('This video has been deleted.', profile.description)
        self.assertEqual('http://seven-pairs.hatenablog.jp/', profile.url)
        self.assertEqual('https://pbs.twimg.com/profile_images/1402804142/icon_400x400.jpg', profile.profile_image_url)
        self.assertEqual('1402804142', profile.user.username)
        self.assertEqual('7pairs', profile.user.first_name)
        self.assertEqual('Jun-ya HASEBA', profile.user.last_name)

    @patch('twingo.backends.API')
    @patch('twingo.backends.OAuthHandler')
    def test_authenticate_02(self, oauth_handler, api):
        """
        [対象] authenticate() : No.02
        [条件] 既存ユーザーでログインする。
        [結果] 該当ユーザーのUserオブジェクトが返却される。
        """
        profile = ProfileFactory()
        api.return_value.me.return_value = TwitterUser(id=profile.twitter_id)

        target = self._get_target_object()
        actual = target.authenticate(('key', 'secret'))

        self.assertEqual(profile.user, actual)

    @patch('twingo.backends.API')
    @patch('twingo.backends.OAuthHandler')
    def test_authenticate_03(self, oauth_handler, api):
        """
        [対象] authenticate() : No.03
        [条件] 無効なユーザーでログインする。
        [結果] Noneが返却される。
        """
        profile = DisableProfileFactory()
        api.return_value.me.return_value = TwitterUser(id=profile.twitter_id)

        target = self._get_target_object()
        actual = target.authenticate(('key', 'secret'))

        self.assertIsNone(actual)

    @patch('twingo.backends.API')
    @patch('twingo.backends.OAuthHandler')
    def test_authenticate_04(self, oauth_handler, api):
        """
        [対象] authenticate() : No.04
        [条件] Twitterからエラーが返却される。
        [結果] Noneが返却される。
        """
        api.return_value.me.side_effect = TweepError('reason')

        target = self._get_target_object()
        actual = target.authenticate(('key', 'secret'))

        self.assertIsNone(actual)

    def test_get_user_01(self):
        """
        [対象] get_user() : No.01
        [条件] 既存ユーザーのIDを指定する。
        [結果] 該当ユーザーのUserオブジェクトが返却される。
        """
        profile = ProfileFactory()

        target = self._get_target_object()
        actual = target.get_user(profile.user.id)

        self.assertEqual(profile.user, actual)

    def test_get_user_02(self):
        """
        [対象] get_user() : No.02
        [条件] 存在しないユーザーのIDを指定する。
        [結果] Noneが返却される。
        """
        profile = ProfileFactory()

        target = self._get_target_object()
        actual = target.get_user(profile.user.id + 1)

        self.assertIsNone(actual)

    def test_get_user_03(self):
        """
        [対象] get_user() : No.03
        [条件] 無効なユーザーのIDを指定する。
        [結果] Noneが返却される。
        """
        profile = DisableProfileFactory()

        target = self._get_target_object()
        actual = target.get_user(profile.user.id)

        self.assertIsNone(actual)
