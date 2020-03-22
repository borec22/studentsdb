from __future__ import unicode_literals

from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

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

@login_required   
def groups_add(request):
    # check if form was posted?
    if request.method == "POST": 
        
        if request.POST.get('add_group_button') is not None:
            
            # validation
            
            errors = {}
            data = {'notes': request.POST.get('notes')}

            title = request.POST.get('title').strip()
            if  not title:
                errors['title'] = _(u"Title of group is required")
            else:
                groups = Group.objects.filter(title = title) 
                if len(groups) > 0:
                    errors['title'] = _(u"This title of group alredy exist.")
                data['title'] = title

            leader = request.POST.get('leader').strip()
            if not leader:
                errors['leader'] = _(u"Choice leader is required")
            else:
                # check or leader is not leader another group
                leaders = Group.objects.filter(leader = leader)
                if len(leaders) == 1:
                    errors['leader'] = _(u"This student is leader another group!") 
                else:
                    data['leader'] = Student.objects.get(pk = request.POST['leader'])
            
            if not errors:
                
                # create new object
                group = Group(**data)

                # save new object(group) to database
                group.save()
                
                # redirect user to list group
                return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('groups'), _(u'Added group %s successfully!' %request.POST['title'] ))) 

            else:
                return render(request, 'groups/groups_add.html', \
                    {'leaders': Student.objects.all().order_by('last_name'), 
                     'errors': errors})

        if request.POST.get('cancel_group_button') is not None:
            # redirect to list group
            return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('groups'), _(u'Adding group has been canceld!')))
    
    else: 
        return render(request, 'groups/groups_add.html', \
                    {'leaders': Student.objects.all().order_by('last_name')})#, \
                     #'errors': errors})
        
    return render (request, 'groups/groups_add.html', \
        {'leaders': Student.objects.all().order_by('last_name')})

#   CLASS FORM AND VIEW PROCEESS EDIT GROUP
    
class GroupUpdateForm(ModelForm):
    class Meta:
        model = Group
        fields = ['title', 'leader', 'notes']

    def __init__(self, *args, **kwargs):
        super(GroupUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

         #set form tag attributes
        #import pdb; pdb.set_trace();
        self.helper.form_action = reverse('groups_edit', kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        #set form field properties
        self.helper.form_tag = True
        self.helper.help_text_inline = True
        self.helper.html5_required = False
        self.helper.form_show_labels = True
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-10'
        self.helper.attrs = {'novalidate': ''}

        
        #add buttons
        self.helper.layout.fields.append(FormActions(
            Submit('save_button', _(u'Save'), css_class="btn btn-primary"),
            Submit('cancel_button_update', _(u'Cancel'), css_class="btn btn-link"),
        ))


class GroupUpdateView(UpdateView):
    model = Group
    template_name = 'groups/groups_edit.html'
    #fields = '__all__'
    form_class = GroupUpdateForm

    def get_success_url(self):
        return u'%s?status_message=%s' % (reverse('groups'), _(u'Updated group successfully!'))

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button_update'):
            return HttpResponseRedirect(
                u'%s?status_message=%s' % (reverse('groups'), _(u'Edding of group has been canceled!')))
        else:
            return super(GroupUpdateView, self).post(request, *args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GroupUpdateView, self).dispatch(*args, **kwargs)
    
@login_required  
def GroupDeleteView(request, gid):

    
    groups = Group.objects.all() 
    #chek was form posted?

    if request.method == 'POST':
        
        # if user check button cancel 
        #import pdb; pdb.set_trace() 
        if request.POST.get('cancel_button_group') is not None:
            print('Hello World')
            
            return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('groups'), _(u'Deleting of group has been canceled!')))
        
        # if uder check button delete
        if request.POST.get('delete_button') is not None:
            
            group = Group.objects.filter(id = gid)

            try:
                group.delete()
            except ProtectedError: 

                message = _(u'Delete group imposible because it has another students!') 
            else:
                message = _(u'Deleted group successfully!') 
            
            # redirect in main page groups
            return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('groups'), message))

    return render(request, 'groups/groups_delete.html', {'groups': groups, 'gid':gid})
