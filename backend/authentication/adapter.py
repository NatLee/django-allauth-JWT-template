from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.urls import reverse
from urllib.parse import urlencode
import json

from django.contrib.auth import get_user_model
from allauth.account.utils import user_email
from allauth.socialaccount.models import SocialAccount

from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import redirect


import logging
logger = logging.getLogger(__name__)

User = get_user_model()

class MyAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        # 檢查是否為社交帳號登入
        auth_methods = request.session.get('account_authentication_methods')
        if auth_methods and auth_methods[0].get('method') == "socialaccount":
            # 獲取 tokens
            tokens = self.get_tokens(request)
            base_url = reverse('social-login-callback')
            query_params = urlencode({'tokens': json.dumps(tokens)})
            return f"{base_url}?{query_params}"
        
        # 如果不是社交帳號登入,使用默認重定向
        return super().get_login_redirect_url(request)

    def get_tokens(self, request):
        from rest_framework_simplejwt.tokens import RefreshToken
        user = request.user
        refresh = RefreshToken.for_user(user)
        return {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):

        social_account = sociallogin.account
        try:
            # 檢查這個社交帳號是否已經綁定了其他帳號
            existing_account = SocialAccount.objects.get(provider=social_account.provider, uid=social_account.uid)
        except SocialAccount.DoesNotExist:
            # 如果社交帳號不存在，繼續檢查 email 是否重複
            existing_account = None

        if sociallogin.state.get('process') == 'login' and existing_account:
            # 如果找到現有的社交帳號，直接返回，允許登入
            return super().pre_social_login(request, sociallogin)

        # 如果現在的process是connect，則不檢查 email
        if sociallogin.state.get('process') == 'connect':
            # 檢查這個社交帳號是否已經綁定了其他帳號
            if existing_account != None:
                if existing_account.user != sociallogin.user:
                    # 這個社交帳號已經綁定了其他帳號
                    logger.warning(f"Social account already connected to another user: {social_account}")
                    # 直接重定向到錯誤頁面
                    raise ImmediateHttpResponse(redirect('social-account-already-connected-by-other'))
                else:
                    # 提示用戶已經綁定了這個社交帳號
                    raise ImmediateHttpResponse(redirect('social-account-already-connected-by-self'))

            return super().pre_social_login(request, sociallogin)

        # 檢查 email 是否重複
        email = user_email(sociallogin.user)
        if email:
            User = get_user_model()
            if User.objects.filter(email=email).exists():
                # Email 已經存在
                logger.warning(f"Duplicate email detected during social login: {email}")
                # 直接重定向到錯誤頁面
                raise ImmediateHttpResponse(redirect('duplicate-email'))

        return super().pre_social_login(request, sociallogin)

    def get_connect_redirect_url(self, request, socialaccount):
        # 處理社交帳號連接的重定向
        base_url = reverse('social-connect-callback')
        return base_url

    def save_user(self, request, sociallogin, form=None):
        # 在這裡，如果 pre_social_login 中發現重複的 email，
        # 程式碼不會執行到這裡，因為會被重定向
        return super().save_user(request, sociallogin, form)