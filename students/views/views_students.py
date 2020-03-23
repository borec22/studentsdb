from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from django.forms import ModelForm, ValidationError
from django.views.generic import UpdateView, DeleteView
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import Field
from crispy_forms.layout import Layout, ButtonHolder, Submit, Button, Fieldset
from crispy_forms.bootstrap import FormActions, AppendedText, PrependedText

from students.models.students_model import Student
from students.models.groups_model import Group
from ..util import paginate, get_current_group


def students_list(request):
    # check if we need to show only one group of students
    current_group = get_current_group(request)
    if current_group:
	    students = Student.objects.filter(student_group=current_group)
    else:
        students = Student.objects.all().order_by('last_name')
	
	#try to order student list
	order_by = request.GET.get('order_by', ' ')
	if order_by in ('last_name', 'first_name', 'ticket', 'id'):
	    students = students.order_by(order_by)
	    if request.GET.get('reverse', '') == '1':
	        students = students.reverse()
	#else:
	#	students = students.order_by('last_name')
	
	#aply pagination, 3 students per page
    context = paginate(students, 3, request, {}, var_name="students")
    return render(request, 'students/students_list.html', context)

@login_required
def students_add(request):
    # was form posted?
    if request.method == "POST":
        #was form add button clicked?
        #import pdb;pdb.set_trace()
        if request.POST.get('add_button') is not None:

            # errors collection
            errors = {}

            # validate student data will go here

            data = {'middle_name': request.POST.get('middle_name'),
                    'notes': request.POST.get('notes')}

            # validata user input
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = _(u"First Name field is required") 
            else:
            	data['first_name'] = first_name

            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
            	errors['last_name'] = _(u"Last Name fieild is required")
            else:
            	data['last_name'] = last_name 

            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
            	errors['birthday'] = _(u"Birthday fieild is required")
            else:
            	try:
            		datetime.strptime(birthday, '%Y-%m-%d')
            	except Exception:
            		errors['birthday'] = _(u"Enter correct formar of data (examp. 1984-12-30)")
            	else:
            		data['birthday'] = birthday
            	data['birthday'] = birthday

            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
            	errors['ticket'] = _(u"Ticket Number is required")
            else:
            	data['ticket'] = ticket

            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
            	errors['student_group'] = _(u'Choice group for student')
            else:
            	groups = Group.objects.filter(pk=student_group)
            	if len(groups) != 1:
            		errors['student_group'] = _(u"Choice correct group")
            	else:	
            	    data['student_group'] = groups[0]

            photo = request.FILES.get('photo')
            if photo:
            	if photo.size > (2048 * 1024):
            		errors['photo'] = _(u"Size of photo must be not more than 2Mb")
            	elif not('image' in photo.content_type):
            		errors['photo'] = _(u"Type of photo that you choiced is not an image")
            	else:
            	    data['photo'] = photo

            # save student
            if not errors:
                #create student object
                student = Student(**data)

                # save it to database
                student.save()

				# redirect user to students list

                return HttpResponseRedirect(u'%s?status_message=%s' %(reverse('home'), _(u"Student %(first_name)s %(last_name)s added successfully!" %({'first_name':student.first_name, 'last_name':student.last_name}) ))) 

            else:
				# render form with errors and previous user input
                return render(request, 'students/students_add.html', {'groups': Group.objects.all().order_by('title'), 'errors': errors})
        elif request.POST.get('cancel_button') is not None:
			# redirect to home page on cancel button
            return HttpResponseRedirect( u'%s?status_message=%s' % (reverse('home'), _(u"Adding of student has been cancelled!")))
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
                raise ValidationError(_(u'Student is a leader another group.'), code='invalid')
            return self.cleaned_data['student_group'] 

    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('students_edit',
            kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.form_tag = True
        self.helper.help_text_inline = True
        self.helper.html5_required = False
        self.helper.form_show_labels = True
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-7'
        self.helper.attrs = {'novalidate': ''}
        #self.helper.layout.append(AppendedText('birthday', '$', active=True))
        self.helper.layout[3] = AppendedText('birthday', '<label for="id_birthday" style="height: 10px"><span class="glyphicon glyphicon-calendar" aria-hidden="true"></span></label>', active=True)
        
        #add buttons
        self.helper.layout.fields.append(FormActions(
            Submit('add_button', _(u'Save'), css_class="btn btn-primary"),
            Submit('cancel_button_student_update', _(u'Cancel'), css_class="btn btn-link"),
        ))

class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/students_edit.html'
    #fields = '__all__'
    form_class = StudentUpdateForm
    
    def get_success_url(self):
        return u'%s?status_message=%s' % (reverse('home'), \
            _(u'Student updated successfully!'))
    
    
    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button_student_update') is not None:
            return HttpResponseRedirect(
                u'%s?status_message=%s' % (reverse('home'), _(u'Editing of student has been cancelled!')))
        else:
            #import pdb; pdb.set_trace()
            return super(StudentUpdateView, self).post(request, *args, **kwargs) 

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StudentUpdateView, self).dispatch(*args, **kwargs)
        
    



class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/student_config_delete.html'

    def get_success_url(self):
        return u'%s?status_message=%s' % (reverse('home'), \
                _(u'Student deleted successfully!'))

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StudentDeleteView, self).dispatch(*args, **kwargs)


    
    
            

    




    



