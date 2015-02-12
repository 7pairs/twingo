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

import factory

from django.contrib.auth.models import User

from twingo.models import Profile


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
    description = None
    profile_image_url = None
    url = None
    user = factory.LazyAttribute(lambda x: UserFactory())


def test_pre_save_profile_01():
    """
    [対象] pre_save_profile()
    [条件] 任意入力の項目をNoneで保存する。
    [結果] Noneのフィールドが空文字に変換される。
    """
    profile = ProfileFactory()

    assert_equal('', profile.description)
    assert_equal('', profile.profile_image_url)
    assert_equal('', profile.url)
