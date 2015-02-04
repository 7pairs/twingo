# -*- coding: utf-8 -*-

"""
Twingoで利用するビューを提供します。

@author: Jun-ya HASEBA
"""

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect

import tweepy


def twitter_login(request):
    """
    ログインURLへのアクセス時に呼び出されます。

    @param request: リクエストオブジェクト
    @type request: django.http.HttpRequest
    @return: 遷移先を示すレスポンスオブジェクト
    @rtype: django.http.HttpResponse
    """
    # TwitterからのコールバックURLを取得
    callback_url = getattr(settings, 'CALLBACK_URL', None)
    if not callback_url:
        callback_url = 'http://%s/callback/' % request.META.get('HTTP_HOST', 'localhost')

    # 認証URLを取得
    oauth_handler = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET, callback_url)
    authorization_url = oauth_handler.get_authorization_url()

    # リクエストトークンをセッションに保存
    request.session['request_token'] = oauth_handler.request_token

    # ログイン後のリダイレクト先URLをセッションに保存
    request.session['next'] = request.GET.get('next')

    # 認証URLにリダイレクト
    return HttpResponseRedirect(authorization_url)


def twitter_callback(request):
    """
    Twitterからのコールバック時に呼び出されます。

    @param request: リクエストオブジェクト
    @type request: django.http.HttpRequest
    @return: 遷移先を示すレスポンスオブジェクト
    @rtype: django.http.HttpResponse
    """
    # セッションからリクエストトークンを取得
    request_token = request.session.get('request_token')
    if not request_token:
        request.session.clear()
        raise PermissionDenied

    # Twitterからの返却値を取得
    oauth_token = request.GET.get('oauth_token')
    oauth_verifier = request.GET.get('oauth_verifier')

    # セッションの値とTwitterからの返却値が一致しない場合は処理続行不可能
    if request_token.get('oauth_token') != oauth_token:
        request.session.clear()
        raise PermissionDenied

    # アクセストークンを取得
    oauth_handler = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    oauth_handler.request_token = request_token
    access_token = oauth_handler.get_access_token(oauth_verifier)

    # 認証処理
    authenticated_user = authenticate(access_token=access_token)

    # ログイン処理
    if authenticated_user:
        login(request, authenticated_user)
    else:
        request.session.clear()
        raise PermissionDenied

    # 認証成功
    top_url = getattr(settings, 'TOP_URL', '/')
    next_url = request.session.get('next', top_url)
    return HttpResponseRedirect(next_url)


def twitter_logout(request):
    """
    ログアウトURLへのアクセス時に呼び出されます。

    @param request: リクエストオブジェクト
    @type request: django.http.HttpRequest
    @return: 遷移先を示すレスポンスオブジェクト
    @rtype: django.http.HttpResponse
    """
    # ログアウト処理
    logout(request)

    # トップページにリダイレクト
    top_url = getattr(settings, 'TOP_URL', '/')
    return HttpResponseRedirect(top_url)
