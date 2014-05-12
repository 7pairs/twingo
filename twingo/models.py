# -*- coding: utf-8 -*-

"""
Twingoで利用するモデルを提供します。

@author: Jun-ya HASEBA
"""

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver


class Profile(models.Model):
    """
    Twitterのユーザー情報を格納するモデルです。
    """

    twitter_id = models.IntegerField(u'Twitter ID', db_index=True, unique=True)
    """Twitter ID"""

    name = models.CharField(u'名前', max_length=20)
    """名前 [例]ちぃといつ"""

    screen_name = models.CharField(u'ユーザー名', max_length=15)
    """ユーザー名 [例]7pairs"""

    description = models.CharField(u'自己紹介', max_length=160, blank=True)
    """自己紹介"""

    profile_image_url = models.URLField(u'プロフィール画像', blank=True)
    """プロフィール画像のURL"""

    url = models.URLField(u'ホームページ', blank=True)
    """ホームページのURL"""

    user = models.ForeignKey(User, verbose_name=u'認証ユーザー', unique=True)
    """Userへの外部キー"""

    create_date = models.DateTimeField(u'登録日時', auto_now_add=True)
    """登録日時"""

    update_date = models.DateTimeField(u'更新日時', auto_now=True)
    """更新日時"""


@receiver(pre_save, sender=Profile)
def pre_save_profile(sender, instance, **kwargs):
    """
    Profileをデータベースに保存する直前に呼び出されます。

    @param sender: モデルクラス
    @type sender: class
    @param instance: 保存するインスタンス
    @type instance: Profile
    @param kwargs: キーワード引数リスト
    @type kwargs: list
    """
    # 自己紹介
    if instance.description is None:
        instance.description = ''

    # プロフィール画像のURL
    if instance.profile_image_url is None:
        instance.profile_image_url = ''

    # ホームページのURL
    if instance.url is None:
        instance.url = ''

