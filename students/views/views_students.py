# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from django.forms import ModelForm, ValidationError
from django.views.generic import UpdateView, DeleteView
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import Field
from crispy_forms.layout import Layout, ButtonHolder, Submit, Button, Fieldset
from crispy_forms.bootstrap import FormActions


from students.models.students_model import Student
from students.models.groups_model import Group


def students_list(request):
	students = Student.objects.all().order_by('last_name')
	
	#try to order student list
	order_by = request.GET.get('order_by', ' ')
	if order_by in ('last_name', 'first_name', 'ticket', 'id'):
	    students = students.order_by(order_by)
	    if request.GET.get('reverse', '') == '1':
	        students = students.reverse()
	#else:
	#	students = students.order_by('last_name')
	
	#paginate students
	paginator = Paginator(students, 3)
	page = request.GET.get('page', '')
	try:
		students = paginator.page(page)
	except PageNotAnInteger:
		#If page is not an integer, deliver first page.
		students = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver
		# last page of results
		students = paginator.page(paginator.num_pages)

	return render(request, 'students/students_list.html', {'students': students})

def students_add(request):
    # was form posted?
    if request.method == "POST":
        #was form add button clicked?
        if request.POST.get('add_button') is not None:

            # errors collection
            errors = {}

            # validate student data will go here

            data = {'middle_name': request.POST.get('middle_name'),
                    'notes': request.POST.get('notes')}

            # validata user input
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = u"Ім'я є обов'язковим" 
            else:
            	data['first_name'] = first_name

            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
            	errors['last_name'] = u"Прізвище є обов'язковим"
            else:
            	data['last_name'] = last_name 

            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
            	errors['birthday'] = u"Дата народження є обов'язковою"
            else:
            	try:
            		datetime.strptime(birthday, '%Y-%m-%d')
            	except Exception:
            		errors['birthday'] = u"Ведіть коректний формат дати (напр. 1984-12-30)"
            	else:
            		data['birthday'] = birthday
            	data['birthday'] = birthday

            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
            	errors['ticket'] = u"Номер білета є обов'язковим"
            else:
            	data['ticket'] = ticket

            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
            	errors['student_group'] = u'Оберіть групу для студента'
            else:
            	groups = Group.objects.filter(pk=student_group)
            	if len(groups) != 1:
            		errors['student_group'] = u"Оберіть коректну групу"
            	else:	
            	    data['student_group'] = groups[0]

            photo = request.FILES.get('photo')
            if photo:
            	if photo.size > (2048 * 1024):
            		errors['photo'] = u"Розмір фотографії не повинен первищувати 2Mb"
            	elif not('image' in photo.content_type):
            		errors['photo'] = u"Тип вибраного вами файлу не є зображенням"
            	else:
            	    data['photo'] = photo

            # save student
            if not errors:
                #create student object
                student = Student(**data)

                # save it to database
                student.save()

				# redirect user to students list

                return HttpResponseRedirect(u'%s?status_message=Студент %s %s успішно доданий!' %(reverse('home'), request.POST['first_name'], request.POST['last_name']))

            else:
				# render form with errors and previous user input
                return render(request, 'students/students_add.html', {'groups': Group.objects.all().order_by('title'), 'errors': errors})
        elif request.POST.get('cancel_button') is not None:
			# redirect to home page on cancel button
            return HttpResponseRedirect( u'%s?status_message=Додавання студента скасовано!' % reverse('home'))
    else:
		# initial form render
        return render(request, 'students/students_add.html', {'groups': Group.objects.all().order_by('title')})

    return render(request, 'students/students_add.html', {'groups': Group.objects.all().order_by('title')})
    
#def students_edit(request, sid):
 #   return HttpResponse('<h1> Edit student %s </h1>' % sid)
    

#class StudentUpdateForm(ModelForm):
#    class Meta:
#        model = Student
#        fields = ['first_name','last_name', 'middle_name', 'birthday',  'photo', 'ticket', 'student_group', 'notes' ]

class StudentUpdateForm(ModelForm):
    class Meta:
        model = Student
        fields = ['first_name','last_name', 'middle_name', 'birthday',  'photo', 'ticket', 'student_group', 'notes' ]

    def clean_student_group(self):
        # get group where current student is a leader
            groups = Group.objects.filter(leader=self.instance)
            if len(groups) > 0 and self.cleaned_data['student_group'] != groups[0]:
                raise ValidationError(u'Студент є старостою іншої групи.', code='invalid')
            return self.cleaned_data['student_group'] 

    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        #self.helper.form_action = reverse('students_edit',
         #   kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.form_tag = True
        self.helper.help_text_inline = True
        self.helper.html5_required = False
        self.helper.form_show_labels = True
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-10'
        self.helper.attrs = {'novalidate': ''}

        
        #add buttons
        self.helper.layout.fields.append(FormActions(
            Submit('save_button', u'Зберегти', css_class="btn btn-primary"),
            Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),
        ))

class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/students_edit.html'
    #fields = '__all__'
    form_class = StudentUpdateForm

    def get_success_url(self):
        return u'%s?status_message=Студента успішно збережено!' \
            % reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(
                u'%s?status_message=Редагування студента відмінено!' %
                reverse('home'))
        else:
            return super(StudentUpdateView, self).post(request, *args, **kwargs) 

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/student_config_delete.html'

    def get_success_url(self):
        return u'%s?status_message=Студента успішно видалено!' % reverse('home')


    
    
            

    




    


