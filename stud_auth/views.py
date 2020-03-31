from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import UpdateView
from .forms import PhotoProfileUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import StProfile
from students.views.views_students import * 

class PhotoProfileUpdateViews(UpdateView):

    form_class = PhotoProfileUpdateForm
    template_name = 'registration/profile_edit.html'
    model = StProfile
	#success_url = reverse_lazy('profile')

    def get_success_url(self):
        return u'%s?status_message=%s' % (reverse_lazy('profile'), \
        	_(u'Profile updated successfully!'))

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel') is not None:
            return HttpResponseRedirect(
                u'%s?status_message=%s' % (reverse_lazy('profile'), _(u'Updated profile canceled!')))
        else:
            return super(PhotoProfileUpdateViews, self).post(request, *args, **kwargs)

def users_list(request):
    users = User.objects.all()
    #try to order users list
    order_by = request.GET.get('order_by', ' ')
    if order_by in ('id', 'last_name', 'first_name', 'username'):
        users = users.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            users = users.reverse()

    #paginate groups
    context = paginate(users, 5, request, {}, var_name="users")
    return render(request, 'users/users_list.html', context)




