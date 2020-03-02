# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
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
from ..util import paginate, get_current_group

#Views for groups    
def groups_list(request):
    # check if we need show only one group
    current_group = get_current_group(request)
    if current_group:
        groups = [current_group]
    else: 
        groups = Group.objects.all()
    #try to order groups list
    order_by = request.GET.get('order_by', '')
    if order_by in ('title',):
        groups = groups.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            groups = groups.reverse()

    #paginate groups
    context = paginate(groups, 2, request, {}, var_name="groups")
    return render (request,'groups/list_group.html', context)

    
def groups_add(request):
    # check if form was posted?
    if request.method == "POST": 
        
        if request.POST.get('add_group_button') is not None:
            
            # validation
            
            errors = {}
            data = {'notes': request.POST.get('notes')}

            title = request.POST.get('title').strip()
            if  not title:
                errors['title'] = u"Назва групи є обов'язковою"
            else:
                groups = Group.objects.filter(title = title) 
                if len(groups) > 0:
                    errors['title'] = u"Дана назва групи вже існує."
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

def groups_edit(request, gid):
    # check groups that checked on page groups with 
    groups = Group.objects.filter(id=gid)

    if request.method == 'POST':

        if request.POST.get('save_button') is not None:

            data = {'notes': request.POST['notes']}
            errors = {}

            """
            title = request.POST.get('title', '').strip()
            if not title:
                errors['title'] = "Назва групи є обов'язковою"
            else:
                data['title'] = request.POST['title']

            leader = request.POST.get('leader').strip()
            if not leader:
                errors[leader] = u"Вибір старости групи є обов'язковим"
            else:
                data['leader'] = Student.objects.get(pk=request.POST['leader']
            """
            title = request.POST.get('title', '').strip()
            if not title:
                errors['title'] = u"Назва групи є обов'язковою"
            else:
                GROUPS = Group.objects.filter(title=request.POST['title'])
                if len(GROUPS) > 0:
                    errors['title'] = u'Дана назва групи вже існує.'
                else:
                    data['title'] = request.POST['title']

            leader = request.POST.get('leader', '').strip()
            if not leader:
                errors['leader'] = u"Вибір старости є обов'язковим"
            else:
                leaders = Group.objects.filter(leader = leader)
                if len(leaders) > 0:
                    errors['leader'] = u"Цей студент є старостою іншої групи!"
                else:
                    data['leader'] = Student.objects.get(pk=request.POST['leader'])

            if not errors:

                group = Group.objects.get(pk=gid)
                group.title = data['title']
                group.leader = data['leader'] #data['leader']
                group.notes = request.POST['notes']  #data['notes']
                group.save()
                #group = Group(
                    #title = request.POST['title'],
                    #leader = Student.objects.get(pk=request.POST['leader']),
                    #notes = request.POST['notes'])

                #group.update()

                return HttpResponseRedirect(u'%s?status_message=Групу успішно збережено!' \
                       % reverse('groups'))

            else:
                return render(request, 'groups/groups_edit.html', \
                    {'id': gid, 'students': Student.objects.all().order_by('last_name'), \
                     'groups': groups, 'errors': errors})

        elif request.POST.get('cancel_button') is not None:
            return HttpResponseRedirect(u'%s?status_message=Редагування групи скасовано.'\
                   % reverse('groups'))
    else:
        return render(request, 'groups/groups_edit.html', \
          {'id': gid, 'students': Student.objects.all().order_by('last_name'), \
           'groups': groups})

    return render(request, 'groups/groups_edit.html', \
           {'id': gid, 'students': Student.objects.all().order_by('last_name'), \
            'groups': groups})

#   CLASS FORM AND VIEW PROCEESS EDIT GROUP
    
#class GroupUpdateForm(ModelForm):
    #class Meta:
        #model = Group
        #fields = ['title', 'leader', 'notes']

    #def __init__(self, *args, **kwargs):
        #super(GroupUpdateForm, self).__init__(*args, **kwargs)

        #self.helper = FormHelper(self)

        # set form tag attributes
        #self.helper.form_action = reverse('groups_edit',
            #kwargs={'pk': kwargs['instance'].id})
        #self.helper.form_method = 'POST'
        #self.helper.form_class = 'form-horizontal'

        # set form field properties
        #self.helper.form_tag = True
        #self.helper.help_text_inline = True
        #self.helper.html5_required = False
        #self.helper.form_show_labels = True
        #self.helper.label_class = 'col-sm-2'
        #self.helper.field_class = 'col-sm-10'
        #self.helper.attrs = {'novalidate': ''}

        
        #add buttons
        #self.helper.layout.fields.append(FormActions(
            #Submit('save_button', u'Зберегти', css_class="btn btn-primary"),
            #Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),
        #))

#class GroupUpdateView(UpdateView):
    #model = Group
    #template_name = 'groups/groups_edit.html'
    #fields = '__all__'
    #form_class = GroupUpdateForm

    #def get_success_url(self):
        #return u'%s?status_message=Групу успішно збережено!' \
            #% reverse('groups')

    #def post(self, request, *args, **kwargs):
        #if request.POST.get('cancel_button'):
            #return HttpResponseRedirect(
                #u'%s?status_message=Редагування групи відмінено!' %
                #reverse('home'))
        #else:
            #return super(GroupUpdateView, self).post(request, *args, **kwargs)
    
    
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
        

#def groups_delete(request, gid):
    #return HttpResponse('<h1> Delete Group %s </h1>' % gid)
