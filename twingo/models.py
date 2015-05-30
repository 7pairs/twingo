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

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver


class Profile(models.Model):
    """
    Twitterのユーザー情報を格納するモデル。
    """

    twitter_id = models.IntegerField(u'Twitter ID', unique=True)
    """Twitter ID"""

    screen_name = models.CharField(u'ユーザー名', max_length=15)
    """ユーザー名"""

    name = models.CharField(u'名前', max_length=20)
    """名前"""

    description = models.CharField(u'自己紹介', max_length=160, blank=True)
    """自己紹介"""

    url = models.URLField(u'ホームページ', blank=True)
    """ホームページのURL"""

    profile_image_url = models.URLField(u'プロフィール画像', blank=True)
    """プロフィール画像のURL"""

    user = models.ForeignKey(User, verbose_name=u'認証ユーザー', unique=True)
    """Userへの外部キー"""

    created_at = models.DateTimeField(u'登録日時', auto_now_add=True)
    """登録日時"""

    updated_at = models.DateTimeField(u'更新日時', auto_now=True)
    """更新日時"""


@receiver(pre_save, sender=Profile)
def pre_save_profile(sender, instance, **kwargs):
    """
    Profileをデータベースに保存する際の前処理。

    :param sender: モデルクラス(ここでは未使用)
    :type sender: Profile
    :param instance: 保存するインスタンス
    :type instance: Profile
    :param kwargs: キーワード引数(ここでは未使用)
    :type kwargs: dict
    """
    # 自己紹介
    if instance.description is None:
        instance.description = ''

    # ホームページのURL
    if instance.url is None:
        instance.url = ''

    # プロフィール画像のURL
    if instance.profile_image_url is None:
        instance.profile_image_url = ''
