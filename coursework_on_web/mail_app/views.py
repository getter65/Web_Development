from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, \
    DeleteView, TemplateView
from django.urls import reverse_lazy, reverse

from blog.models import Post
from mail_app.forms import MailingForm
from mail_app.models import Mailing, Client, MailingAttempt, Message
from mail_app.services import get_objects_from_cache


class MailingListView(ListView):
    model = Mailing

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm('mail_app.view_mailing'):
            return queryset
        return queryset.filter(owner=self.request.user)


class MailingAttemptListView(ListView):
    model = MailingAttempt
    template_name = 'mail_app/mailing_attempt_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm('mail_app.view_mailingattempt'):
            return queryset
        return queryset.filter(mailing__owner=self.request.user)


class MailingDetailView(DetailView):
    model = Mailing

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.has_perm('mail_app.view_mailing') or self.request.user == self.object.owner:
            return self.object
        raise HttpResponseForbidden


class MailingCreateView(CreateView):
    model = Mailing
    # fields = ('time', 'frequency', 'message', 'recipient')
    form_class = MailingForm
    success_url = reverse_lazy('mail_app:mailing_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['recipient'].queryset = Client.objects.filter(user=self.request.user)
        return context

    def form_valid(self, form):
        mailing = form.save()
        mailing.owner = self.request.user
        mailing.save()
        return super().form_valid(form)


class MailingUpdateView(UserPassesTestMixin, UpdateView):
    model = Mailing
    fields = ('time', 'frequency')

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('mail_app:update_mailing', kwargs={'pk': pk})

    def test_func(self):
        mailing = self.get_object()
        return self.request.user == mailing.owner or self.request.user.has_perm(perm='mail_app.change_mailing')


class MailingDeleteView(UserPassesTestMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mail_app:index')

    def test_func(self):
        mailing = self.get_object()
        return self.request.user == mailing.owner or self.request.user.has_perm(perm='mail_app.delete_mailing')


@permission_required('mail_app.set_status')
def stop_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if mailing.status == Mailing.STARTED:
        mailing.status = Mailing.FINISHED
    mailing.save()
    return redirect(request.META.get('HTTP_REFERER'))


class ClientListView(ListView):
    model = Client

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm('mail_app.set_status'):
            return queryset
        return queryset.filter(user=self.request.user)


class ClientCreateView(CreateView):
    model = Client
    fields = ('email', 'full_name', 'comments')
    success_url = reverse_lazy('mail_app:clients')

    def form_valid(self, form):
        client = form.save()
        client.user = self.request.user
        client.save()
        return super().form_valid(form)


class ClientUpdateView(UserPassesTestMixin, UpdateView):
    model = Client
    fields = ('email', 'full_name', 'comments')
    success_url = reverse_lazy('mail_app:clients')

    def test_func(self):
        client = self.get_object()
        return self.request.user in [c.owner for c in client.mailing_set] or self.request.user.has_perm(perm='mail_app.change_client')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mail_app:clients')

    def test_func(self):
        client = self.get_object()
        return self.request.user in [c.owner for c in client.mailing_set] or self.request.user.has_perm(perm='mail_app.delete_client')


class MessageCreateView(CreateView):
    model = Message
    fields = ('topic', 'body',)
    success_url = reverse_lazy('mail_app:messages')

    def form_valid(self, form):
        message = form.save()
        message.user = self.request.user
        message.save()
        return super().form_valid(form)


class MessageListView(ListView):
    model = Message

    def get_queryset(self):
        queryset = get_objects_from_cache(Message, 'messages')
        if self.request.user.has_perm('mail_app.set_status'):
            return queryset
        return queryset.filter(user=self.request.user)


class MessageUpdateView(UserPassesTestMixin, UpdateView):
    model = Message
    fields = ('topic', 'body',)
    success_url = reverse_lazy('mail_app:messages')

    def test_func(self):
        message = self.get_object()
        return self.request.user == message.user or self.request.user.has_perm(perm='mail_app.change_message')


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mail_app:messages')

    def test_func(self):
        message = self.get_object()
        return self.request.user == message.user or self.request.user.has_perm(perm='mail_app.change_message')


class IndexTemplateView(TemplateView):
    template_name = 'mail_app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing_total'] = Mailing.objects.count()
        context['mailing_active'] = Mailing.objects.filter(status=Mailing.STARTED).count()
        context['clients'] = Client.objects.distinct().count()
        context['blog'] = Post.objects.order_by('?')[:3]
        return context


