# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import Field
from crispy_forms.layout import Layout, ButtonHolder, Submit, Button, Fieldset
from crispy_forms.bootstrap import FormActions, AppendedText, PrependedText

from django import forms
from django.views.generic import UpdateView, DeleteView, CreateView
from django.forms import ModelForm
from students.models.exams_model import Exam
from students.models.groups_model import Group
from students.models.students_model import Student
from ..util import paginate, get_current_group 

#Views for groups  

def exam_list(request):
    current_group = get_current_group(request)
    if current_group:
        exams = Exam.objects.filter(examenation = current_group)
    else:
        exams = Exam.objects.all()
    #try to order exams list
    order_by = request.GET.get('order_by', '')
    if order_by in ('subject','teacher',):
        exams = exams.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            exams = exams.reverse()

    #paginate exams
    context = paginate(exams, 3, request, {}, var_name="exams")
    return render (request, 'exams/exam_list.html', context)


class EditExamForm(forms.ModelForm):

    subject = forms.CharField(max_length=100,
                 label = _(u'Subject'),
                 widget = forms.TextInput
                 (attrs={'placeholder': _(u'Enter name of subject')}))

    data_and_time = forms.DateTimeField(label = _(u'Data and time'),
                 input_formats=["%d/%m/%Y %H:%M:%S"],
                 widget = forms.DateTimeInput( 
                    attrs={'placeholder':"DD/MM/YYYY HH:MM:SS"}
                 #attrs={'placehilder': 'Дата та час'})
                 ))
    teacher = forms.CharField(max_length=100,
                 label = _(u'Teacher'),
                 widget = forms.TextInput
                 (attrs={'placeholder': _(u'Enter last name/first name/middle name of teacher')}))

    examenation = forms.ModelMultipleChoiceField(
                 label= _(u'Take of exam'),
                 widget = forms.CheckboxSelectMultiple(),
                 queryset = Group.objects.all().order_by('title')
                 )

    class Meta:
        model = Exam
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EditExamForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        #import pdb;pdb.set_trace();
        self.helper.form_action = reverse('exam_edit',
            kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.form_tag = True
        self.helper.help_text_inline = True
        self.helper.html5_required = False
        self.helper.form_show_labels = True
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-6'
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout[1] = AppendedText('data_and_time', '<label for="id_data_and_time" \
            style="height: 10px"> <span class="glyphicon glyphicon-calendar" \
            aria-hidden="true"> </span> </label>', active=True)

        
        #add buttons
        self.helper.layout.fields.append(FormActions(
            Submit('save_button', _(u'Save'), css_class="btn btn-primary"),
            Submit('cancel_button', _(u'Cancel'), css_class="btn btn-link"),
        ))

class exam_edit(UpdateView):
    model = Exam
    form_class = EditExamForm
    template_name = 'exams/exams_edit.html'

    def get_success_url(self):
        return u'%s?status_message=%' % (reverse('exam'), _(u'Updated exam successfully'))

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('exam'), _(u'Edding of exam has been canceled!')))
        else:
            return super(exam_edit, self).post(request, *args, **kwargs)

    

class exam_delete(DeleteView):
    model = Exam
    #form_class = DeleteExamForm
    template_name = 'exams/exams_delete.html'

    def get_success_url(self):
        return u'%s?status_message=%s' % (reverse('exam'), _(u'Delete exam successfully!'))

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button') is not None:
            return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('exam'), _(u'Deleting of exam has been canceled!')))
        else:
            return super(exam_delete, self).post(request, *args, **kwargs)


class AddExamForm(forms.ModelForm):

    subject = forms.CharField(max_length=100,
                 label = _(u'Subject'),
                 widget = forms.TextInput
                 (attrs={'placeholder': _(u'Enter name of subject')}))

    data_and_time = forms.DateTimeField(label = _(u'Data and time'),
                 input_formats=["%d/%m/%Y %H:%M:%S"],
                 widget = forms.DateTimeInput( 
                    attrs={'placeholder':"DD/MM/YYYY HH:MM:SS"}
                 #attrs={'placehilder': 'Дата та час'})
                 ))
    teacher = forms.CharField(max_length=100,
                 label = _(u'Teacher'),
                 widget = forms.TextInput
                 (attrs={'placeholder': _(u'Enter last name/first name/middle name of teacher')}))

    examenation = forms.ModelMultipleChoiceField(
                 label= _(u'Take of exam'),
                 widget = forms.CheckboxSelectMultiple(),
                 queryset = Group.objects.all().order_by('title')
                 )

    class Meta:
        model = Exam
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AddExamForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        
        #import pdb;pdb.set_trace();
        self.helper.form_action = reverse('add_exam')
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.form_tag = True
        self.helper.help_text_inline = True
        self.helper.html5_required = False
        self.helper.form_show_labels = True
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-5'
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout[1] = AppendedText('data_and_time', '<label for="id_data_and_time" \
            style="height: 10px"> <span class="glyphicon glyphicon-calendar" \
            aria-hidden="true"> </span> </label>', active=True)

        
        #add buttons
        self.helper.layout.fields.append(FormActions(
            Submit('add_button', _(u'Add'), css_class="btn btn-primary"),
            Submit('cancel_button', _(u'Сancel'), css_class="btn btn-link"),
        ))

class add_exam(CreateView):
    model = Exam
    form_class = AddExamForm
    template_name = 'exams/exams_add.html'

    def get_success_url(self):
        return u'%s?status_message=%' % (reverse('exam'), _(u'Exam added successfully!'))

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('exam'), _(u'Adding of exam has been canceled!')))
        else:
            return super(add_exam, self).post(request, *args, **kwargs)



      
