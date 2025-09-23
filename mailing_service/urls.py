from django.urls import path

from .apps import MailingServiceConfig
from .views import RecipientCreateView, RecipientListView, RecipientDeleteView, RecipientDetailView, \
    RecipientUpdateView, MessageListView, MessageCreateView, MessageDeleteView, MessageDetailView, MessageUpdateView, \
    MailingCreateView, MailingDetailView, MailingUpdateView, MailingListView, MailingDeleteView, MailingSendView, \
    HomePageView

app_name = MailingServiceConfig.name

urlpatterns = [
    path('home/', HomePageView.as_view(), name='home'),
    path('recipients_list/', RecipientListView.as_view(), name='recipients_list'),
    path('recipient_create/', RecipientCreateView.as_view(), name='recipient_create'),
    path('recipient_detail/<int:pk>/', RecipientDetailView.as_view(), name='recipient_detail'),
    path('recipient_update/<int:pk>/', RecipientUpdateView.as_view(), name='recipient_update'),
    path('recipient_delete/<int:pk>/', RecipientDeleteView.as_view(), name='recipient_delete'),
    path('messages_list/', MessageListView.as_view(), name='messages_list'),
    path('message_create/', MessageCreateView.as_view(), name='message_create'),
    path('message_detail/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message_update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message_delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
    path('mailings_list/', MailingListView.as_view(), name='mailings_list'),
    path('mailing_create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing_detail/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing_update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing_delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailing_send/<int:pk>/', MailingSendView.as_view(), name='mailing_send'),
]