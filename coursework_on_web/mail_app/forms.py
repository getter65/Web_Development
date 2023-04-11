from django import forms

from mail_app.models import Mailing


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        exclude = ('owner',)