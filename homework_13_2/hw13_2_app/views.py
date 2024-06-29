from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RegisterForm, LoginForm


class SignUpUserView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('hw10_app:home')
        form = RegisterForm()
        return render(request, 'hw13_2_app/signup.html', {'form': form})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('hw10_app:home')
        
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hw10_app:home')
        return render(request, 'hw13_2_app/signup.html', {'form': form})


class LoginUserView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('hw10_app:home')
        form = LoginForm()
        return render(request, 'hw13_2_app/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('hw10_app:home')

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is None:
            messages.error(request, 'Username or password didn\'t match')
            return redirect('hw13_2_app:login')

        login(request, user)
        return redirect('hw10_app:home')
    

class LogoutUserView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('hw10_app:home')


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'hw13_2_app/password_reset.html'
    email_template_name = 'hw13_2_app/password_reset_email.html'
    html_email_template_name = 'hw13_2_app/password_reset_email.html'
    success_url = reverse_lazy('hw13_2_app:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'hw13_2_app/password_reset_subject.txt'
