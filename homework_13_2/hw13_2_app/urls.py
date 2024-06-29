from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, reverse_lazy

from .views import SignUpUserView, LoginUserView, LogoutUserView, ResetPasswordView

app_name = 'hw13_2_app'

urlpatterns = [
    path('signup/', SignUpUserView.as_view(), name='signup'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('reset-password/', ResetPasswordView.as_view(), name='password_reset'),
    path('reset-password/done/', PasswordResetDoneView.as_view(template_name='hw13_2_app/password_reset_done.html'),
         name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='hw13_2_app/password_reset_confirm.html',
                                          success_url=reverse_lazy('hw13_2_app:password_reset_complete')),
         name='password_reset_confirm'),
    path('reset-password/complete/',
         PasswordResetCompleteView.as_view(template_name='hw13_2_app/password_reset_complete.html'),
         name='password_reset_complete'),
]

