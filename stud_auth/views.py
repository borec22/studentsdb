from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import UpdateView
from .forms import PhotoProfileUpdateForm
from .models import StProfile

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




