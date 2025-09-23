from django.urls import path

from .views import UserRegisterView, UserLoginView, UserLogout, confirm_email_view, DisableMailingView, BlockUserView, \
    UsersListView
from .apps import UsersConfig
from django.contrib.auth import views as auth_views


app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('confirm/<str:signed_email>/', confirm_email_view, name='confirm_email'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html',
        email_template_name='users/password_reset_email.html',
        success_url='/users/password_reset_done/'
    ), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html',
        success_url='/users/reset/done/'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('disable/<int:pk>/', DisableMailingView.as_view(), name='disable_mailing'),
    path('block/<int:pk>/', BlockUserView.as_view(), name='block_user'),
    path('users_list/', UsersListView.as_view(), name='users_list'),
]