# -*- coding: utf-8 -*-
from collections import OrderedDict

from django.shortcuts import render
from django import forms
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages

from studentsdb.settings import ADMIN_EMAIL
from django.views.generic.edit import FormView
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from contact_form.forms import ContactForm

class CustomContactForm(ContactForm):
    def __init__(self, request, *args, **kwargs):
        super(CustomContactForm, self).__init__(request=request, *args, **kwargs)
        fields_keyOrder = ['reason', 'name', 'email', 'body']
        if (self.fields.has_key('keyOrder')):
            self.fields.keyOrder = fields_keyOrder
        else:
            self.fields = OrderedDict((k, self.fields[k]) for k in fields_keyOrder)
 
    REASON = (
        ('support', 'Support'),
        ('feedback', 'Feedback'),
        ('delete', 'Account deletion')
    )
    reason = forms.ChoiceField(choices=REASON, label='Reason')
    #captcha = CaptchaField()
    template_name = 'contact_admin/django_contact_form.txt'
    subject_template_name = "contact_admin/django_contact_form_subject.txt"

class CustomContactFormView(FormView):
    form_class = CustomContactForm
    template_name = 'contact_admin/django_contact_form.html'
    success_url = reverse_lazy('contact_form_sent')

    def form_valid(self, form):
        form.save()
        return super(CustomContactFormView, self).form_valid(form)

    def get_form_kwargs(self):
        # ContactForm instances require instantiation with an
        # HttpRequest.
        kwargs = super(CustomContactFormView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    #def get_success_url(self):
        # This is in a method instead of the success_url attribute
        # because doing it as an attribute would involve a
        # module-level call to reverse(), creating a circular
        # dependency between the URLConf (which imports this module)
        # and this module (which would need to access the URLConf to
        # make the reverse() call).
        #return reverse_lazy('contact_form_sent')

