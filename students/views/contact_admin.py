# -*- coding: utf-8 -*-
import logging
from django.shortcuts import render
from django import forms
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from django.views.generic.edit import FormView
from studentsdb.settings import ADMIN_EMAIL
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class ContactForm(forms.Form):
    from_email = forms.EmailField(
        label=u"Ваша Емейл Адреса")

    subject = forms.CharField(
        label=u"Заголовок листа",
        max_length=128)

    message = forms.CharField(
    	label=u"Текст повідомлення",
    	max_length=2560,
    	widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        #call original initializator
        super(ContactForm, self).__init__(*args, **kwargs)

        # this helper object allows us to customize form
        self.helper = FormHelper()

        # form tag attributes
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('contact_admin')

        # twitter botstarp styles 
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # form buttons
        self.helper.add_input(Submit('second_button', u'Надіслати'))

#contact_admin by class FormView
class ContactAdminView(FormView):
    template_name = 'contact_admin/form.html'
    form_class = ContactForm
    success_url = 'students/students_list'

    def get_success_url(self):
        return u'%s?status_message=Повідомлення успішно відправлено!' % reverse('contact_admin')

    def form_valid(self, form):
        """This method is called for valid data"""
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        #import pdb; pdb.set_trace()
        from_email = form.cleaned_data['from_email']

        try:
            send_mail(subject, message, [from_email], ['romanchuk.sss22121999@gmail.com'])

        except Exception:
            message="Під час відправки листа виникла помилка. Спробуйте будь-ласка пізніше."
            logger = logging.getLogger(__name__)
            logger.exception(message)

        return super(ContactAdminView, self).form_valid(form)

#contact admin by view

#def contact_admin(request):
    # check if form was posted
    #if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        #form = ContactForm(request.POST)
        # check whether user data is valid:
        #if form.is_valid():
            # send email
            #subject = form.cleaned_data['subject'] 
            #message = form.cleaned_data['message']
            #from_email = form.cleaned_data['from_email']

            
            #try:
                #send_mail(subject, message, [from_email], [ADMIN_EMAIL]) #fail_silentle=False)

            #except BadHeaderError:
               # message = u"Під час відправки листа виникла непередбачувана помилка. "\
                         # u"Спробуйте скористатись даною формою пізніше."
           # else: 
                #message = u"Повідомлення успішно надіслане!"

            # redirect to same contact page with sucsess message
            
            #return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('contact_admin'), message))
        
        
    # if there was not POST render blank form
    #else:
        #form = ContactForm()
    
    #return render(request, 'contact_admin/form.html', {'form': form})