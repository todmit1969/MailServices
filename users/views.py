from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.views.generic import FormView, ListView
from mailing_service.models import Mailing
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
from django.contrib.auth import login, get_user_model
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired

from .models import CustomUser
import os

signer = TimestampSigner()


class UserRegisterView(FormView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('mailing_service:home')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        self.send_confirmation_email(user)
        return render(self.request, 'users/email_sent.html', {'email': user.email})

    def send_confirmation_email(self, user):
        signed_email = signer.sign(user.email)
        confirm_url = self.request.build_absolute_uri(
            reverse_lazy('users:confirm_email', kwargs={'signed_email': signed_email})
        )
        subject = 'Подтверждение регистрации'
        message = f'Перейдите по ссылке для подтверждения регистрации: {confirm_url}'
        from_email = os.getenv("EMAIL_HOST_USER")
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)


def confirm_email_view(request, signed_email):
    try:
        email = signer.unsign(signed_email, max_age=60*60*24)
        user = CustomUser.objects.get(email=email)
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'users/email_confirmed.html')
    except (BadSignature, SignatureExpired):
        return render(request, 'users/email_invalid.html')


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('mailing_service:home')


class UsersListView(ListView):
    model = CustomUser
    template_name = 'users/users_list.html'
    context_object_name = 'users'


class UserLogout(LogoutView):
    template_name = 'users/logout.html'
    next_page = reverse_lazy('users:logout')


User = get_user_model()


class BlockUserView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_manager()

    def post(self, request, *args, **kwargs):
        user_to_block = get_object_or_404(User, pk=kwargs['pk'])
        if user_to_block.is_superuser or user_to_block == request.user:
            return redirect('users:user_list')

        user_to_block.is_active = False
        user_to_block.save()
        return redirect('users:user_list')


class DisableMailingView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_manager()

    def post(self, **kwargs):
        mailing = get_object_or_404(Mailing, pk=kwargs['pk'])
        mailing.status = 'Завершена'
        mailing.save()
        return redirect('mailing:mailing_list')