from django.contrib.auth.decorators import login_required
from django.urls import path

from mail_app.apps import MailAppConfig
from mail_app.views import MailingListView, MailingCreateView, \
    ClientCreateView, ClientUpdateView, ClientDeleteView, MailingUpdateView, \
    MailingDeleteView, ClientListView, MailingDetailView, MailingAttemptListView, stop_mailing, MessageListView, \
    MessageCreateView, MessageUpdateView, MessageDeleteView

app_name = MailAppConfig.name

urlpatterns = [
    path('mailings/', login_required(MailingListView.as_view()), name='mailing_list'),
    path('<int:pk>/', login_required(MailingDetailView.as_view()), name='mailing_card'),
    path('create_mailing/', login_required(MailingCreateView.as_view()), name='create_mailing'),
    path('update_mailing/<int:pk>/', login_required(MailingUpdateView.as_view()), name='update_mailing'),
    path('delete_mailing/<int:pk>/', login_required(MailingDeleteView.as_view()), name='delete_mailing'),
    path('stop_mailing/<int:pk>/', stop_mailing, name='stop_mailing'),
    path('clients/', login_required(ClientListView.as_view()), name='clients'),
    path('create_client/', login_required(ClientCreateView.as_view()), name='create_client'),
    path('update_client/<int:pk>/', login_required(ClientUpdateView.as_view()), name='update_client'),
    path('delete_client/<int:pk>/', login_required(ClientDeleteView.as_view()), name='delete_client'),
    path('mailing_attempt_list/', login_required(MailingAttemptListView.as_view()), name='mailing_attempt_list'),
    path('messages/', login_required(MessageListView.as_view()), name='messages'),
    path('create_message/', login_required(MessageCreateView.as_view()), name='create_message'),
    path('update_message/<int:pk>/', login_required(MessageUpdateView.as_view()), name='update_message'),
    path('delete_message/<int:pk>/', login_required(MessageDeleteView.as_view()), name='delete_message'),
]