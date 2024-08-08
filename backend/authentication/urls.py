from django.urls import path, include
from authentication import views

urlpatterns = [
    path('', include('allauth.urls')),

    path('social/login/callback', views.social_login_callback, name='social-login-callback'),
    path('social/connect/callback', views.social_connect_callback, name='social-connect-callback'),
    path('social/exceptions/duplicate-email', views.duplicate_email, name='duplicate-email'),
    path('social/exceptions/social-account-already-connected-by-other', views.social_account_already_connected_by_other, name='social-account-already-connected-by-other'),
    path('social/exceptions/social-account-already-connected-by-self', views.social_account_already_connected_by_self, name='social-account-already-connected-by-self'),
    path('social/exceptions/connect-social-account-without-login', views.connect_social_account_without_login, name='connect-social-account-without-login'),

    path('social/accounts', views.SocialAccountListView.as_view(), name='social-account-list'),
    path('logout', views.LogoutView.as_view(), name='auth-logout'),

]
