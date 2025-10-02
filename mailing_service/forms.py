from django import forms
from django.core.exceptions import ValidationError

from .models import Mailing, Recipient, Message


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['start_datetime', 'end_datetime', 'message', 'recipients']
        widgets = {
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'recipients': forms.SelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)

        self.fields['start_datetime'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['end_datetime'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['message'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['recipients'].widget.attrs.update({
            'class': 'form-control'
        })


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['email', 'full_name', 'comment']

    def __init__(self, *args, **kwargs):
        super(RecipientForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите свой email'
        })

        self.fields['full_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите Ф.И.О.'
        })

        self.fields['comment'].widget.attrs.update({
            'class': 'form-control',
            'type': 'str'
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('email надо указать!')
        return email


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'letter']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        self.fields['subject'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Тема'
        })

        self.fields['letter'].widget.attrs.update({
            'class': 'form-control',
            'type': 'str'
        })