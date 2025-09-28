from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import MailingForm, RecipientForm, MessageForm
from .models import Recipient, Message, Mailing, SendAttempt


@method_decorator(cache_page(60 * 15), name='dispatch')
class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        mailings = Mailing.objects.filter(owner=user)

        context['total_mailings'] = Mailing.objects.count()
        context['active_mailings'] = Mailing.objects.filter(status='Запущена').count()
        context['unique_recipients'] = Recipient.objects.count()
        context['success_attempts'] = SendAttempt.objects.filter(mailing__in=mailings, status='Успешно').count()
        context['failed_attempts'] = SendAttempt.objects.filter(mailing__in=mailings, status='Не успешно').count()
        return context


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'recipient_create.html'
    success_url = reverse_lazy('mailing_service:recipients_list')


@method_decorator(cache_page(60 * 15), name='dispatch')
class RecipientDetailView(DetailView):
    model = Recipient
    template_name = 'recipient_detail.html'
    context_object_name = 'recipient'


class RecipientUpdateView(UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'recipient_create.html'
    success_url = reverse_lazy('mailing_service:recipients_list')


class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = 'recipient_delete.html'
    success_url = reverse_lazy('mailing_service:recipients_list')


@method_decorator(cache_page(60 * 15), name='dispatch')
class RecipientListView(ListView):
    model = Recipient
    template_name = 'recipients_list.html'
    context_object_name = 'recipients'


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'message_create.html'
    success_url = reverse_lazy('mailing_service:messages_list')


@method_decorator(cache_page(60 * 15), name='dispatch')
class MessageDetailView(DetailView):
    model = Message
    template_name = 'message_detail.html'
    context_object_name = 'message'


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'message_create.html'
    success_url = reverse_lazy('mailing_service:messages_list')


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'message_delete.html'
    success_url = reverse_lazy('mailing_service:messages_list')


@method_decorator(cache_page(60 * 15), name='dispatch')
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'messages_list.html'
    context_object_name = 'messages'


@method_decorator(cache_page(60 * 15), name='dispatch')
class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailings_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        user = self.request.user
        if user.is_manager():
            queryset = Mailing.objects.all()
        else:
            queryset = Mailing.objects.filter(owner=user)

        for mailing in queryset:
            mailing.update_status()
        return queryset


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_create.html'
    success_url = reverse_lazy('mailing_service:mailings_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.update_status()
        return response


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_create.html'
    success_url = reverse_lazy('mailing_service:mailings_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.update_status()
        return response

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user.is_manager() and obj.owner != self.request.user:
            raise PermissionDenied("Менеджер не может редактировать чужие рассылки.")
        elif obj.owner != self.request.user:
            raise PermissionDenied("Вы не можете редактировать чужую рассылку.")
        return obj


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing_delete.html'
    success_url = reverse_lazy('mailing_service:mailings_list')


@method_decorator(cache_page(60 * 15), name='dispatch')
class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing_detail.html'
    context_object_name = 'message'


class MailingSendView(View):
    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        mailing.send()
        messages.success(request, f"Рассылка #{mailing.id} отправлена вручную.")
        return redirect('mailing_service:mailings_list')