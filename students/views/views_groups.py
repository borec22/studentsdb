# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import UpdateView, DeleteView
from django.forms import ModelForm
from django.db.models import ProtectedError

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import Field
from crispy_forms.layout import Layout, ButtonHolder, Submit, Button, Fieldset
from crispy_forms.bootstrap import FormActions

from students.models.groups_model import Group
from students.models.students_model import Student

#Views for groups    
def groups_list(request):
    groups = Group.objects.all()

    #try to order groups list
    order_by = request.GET.get('order_by', '')
    if order_by in ('title',):
        groups = groups.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            groups = groups.reverse()

    #paginate groups
    paginator = Paginator(groups, 2)
    page = request.GET.get('page', '')
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        #If page is not an integer, deliver first page.
        groups = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver
        # last page of results
        groups = paginator.page(paginator.num_pages)
    return render (request,'groups/list_group.html', {'groups': groups})

    
def groups_add(request):
    # check if form was posted?
    if request.method == "POST": 
        
        if request.POST.get('add_group_button') is not None:
            
            # to do validation
            # перевіряємо на коректність даних і збираємо помилки
            errors = {}
            data = {'notes': request.POST.get('notes')}

            title = request.POST.get('title').strip()
            if  not title:
                errors['title'] = u"Назва групи є обов'язковою"
            else:
                data['title'] = title

            leader = request.POST.get('leader').strip()
            if not leader:
                errors['leader'] = u"Вибір старости групи є обов'язковим"
            else:
                # check or leader is not leader another group
                leaders = Group.objects.filter(leader = leader)
                if len(leaders) == 1:
                    errors['leader'] = u"Цей студент є старостою іншої групи!" 
                else:
                    data['leader'] = Student.objects.get(pk = request.POST['leader'])
            
            if not errors:
                
                # create new object
                group = Group(**data)

                # save new object(group) to database
                group.save()
                
                # redirect user to list group
                return HttpResponseRedirect(u'%s?status_message=Групу %s успішно додано!' \
                       % (reverse('groups'), request.POST['title']))

            else:
                return render(request, 'groups/groups_add.html', \
                    {'leaders': Student.objects.all().order_by('last_name'), 
                     'errors': errors})

        if request.POST.get('cancel_group_button') is not None:
            # redirect to list group
            return HttpResponseRedirect(u'%s?status_message=Додавання групи скасовано!' % reverse('groups'))
    
    else: 
        return render(request, 'groups/groups_add.html', \
                    {'leaders': Student.objects.all().order_by('last_name')})#, \
                     #'errors': errors})
        
    return render (request, 'groups/groups_add.html', \
        {'leaders': Student.objects.all().order_by('last_name')})
    
class GroupUpdateForm(ModelForm):
    class Meta:
        model = Group
        fields = ['title', 'leader', 'notes']

    def __init__(self, *args, **kwargs):
        super(GroupUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('groups_edit',
            kwargs={'pk': kwargs['instance'].id})
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

class GroupUpdateView(UpdateView):
    model = Group
    template_name = 'groups/groups_edit.html'
    #fields = '__all__'
    form_class = GroupUpdateForm

    def get_success_url(self):
        return u'%s?status_message=Групу успішно збережено!' \
               % reverse('groups')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_group_button'):
            return HttpResponseRedirect(u'%s?status_message=Редагування групи скасовано!' \
                                       % reverse('groups'))
        else:
            return super(GroupUpdateView, self).post(request, *args, **kwargs)

    
def GroupDeleteView(request, gid):
    groups = Group.objects.all() 
    #chek was form posted?
    if request.method == 'POST':
            
        # if uder check button delete
        if request.POST.get('delete_button') is not None:
            

            group = Group.objects.filter(id = gid)

            try: 
                group.delete()
            except ProtectedError: 

                message = u'Видалення групи не можливо, оскільки в ній присутні інші студенти!' 
            else:
                message = u'Групу успішно видалено!' 
            
            # redirect in main page groups
            return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('groups'), message))

        # if user check button cancel
        elif request.POST.get('cancel_button') is not None:
            return HttpResponseRedirect(u'%s?status_message=Видалення групи скасовано' % reverse('groups'))

    return render(request, 'groups/groups_delete.html', {'groups': groups, 'gid':gid})



            # check whether user data is valid


        #return u'%s?status_message=Групу успішно видалено!' % reverse('groups')
        

def groups_delete(request, gid):
    return HttpResponse('<h1> Delete Group %s </h1>' % gid)
