"""studentsdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from students.views.views_students import * 
from students.views.views_groups import *
from students.views.views_journal import *
from students.views.views_exam import *
from students.views.contact_admin import *
from students.views.django_contact_admin import *
from students.views.user_profile import *
from stud_auth.views import *

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import admin
from django.conf.urls import url, include
from django.views.i18n import javascript_catalog
from django.contrib.auth import views as auth_views

from django.views.generic import RedirectView, TemplateView
from .settings import MEDIA_ROOT, DEBUG
from django.conf import settings
from django.conf.urls.static import static

js_info_dict = {
    'packages': ('students',),
}

urlpatterns = [
    # Students urls
    url(r'^$', students_list, name='home'),
    url(r'^students/add/$', permission_required('students.add_student')(students_add), name='students_add'),
    url(r'^students/(?P<pk>\d+)/edit/$', permission_required('students.change_student')(StudentUpdateView.as_view()), name='students_edit'),
    url(r'^students/(?P<pk>\d+)/delete/$', StudentDeleteView.as_view(), name='students_delete'),
     
    #Groups urls
    url(r'^groups/$', login_required(groups_list), name='groups'),
    url(r'^groups/add/$', login_required(groups_add), name='groups_add'),  
    url(r'^groups/(?P<pk>\d+)/edit/$', login_required(GroupUpdateView.as_view()), name='groups_edit'),
    url(r'^groups/(?P<gid>\d+)/delete/$', login_required(GroupDeleteView), name='groups_delete'),
    

    #Journal urls
    url(r'^journal/(?P<pk>\d+)?/?$', JournalView.as_view(), name='journal'),

    #Exam urls
    url(r'^exam/$', login_required(exam_list), name='exam'),
    url(r'^exam/(?P<pk>\d+)/edit_exam/$', login_required(exam_edit.as_view()), name='exam_edit'),
    url(r'^exam/(?P<pk>\d+)/delete_exam/$', login_required(exam_delete.as_view()), name='exam_delete'),
    url(r'^exam/add/$', login_required(add_exam.as_view()), name='add_exam'),

    # Contact Admin Form
    url(r'^contact-admin/$', ContactAdminView.as_view(), name='contact_admin'),
    # Contact admin by help django application django-contact-form
    url(r'^django-contact-admin/$', CustomContactFormView.as_view(), name='django-contact-admin'),
    url(r'^contact/sent/$', TemplateView.as_view(
            template_name='contact_admin/django_contact_form_sent.html'),
            name='contact_form_sent'),

    # User Related urls
    url(r'^users/profile/$', login_required(TemplateView.as_view(
        template_name='registration/profile.html')), name='profile'),
    url(r'^users/profile/(?P<pk>[\d]+)/edit/$', PhotoProfileUpdateViews.as_view(), name='profile_edit'),
    url(r'^users/logout/$', auth_views.logout, kwargs={'next_page': 'home'}, \
                                               name='auth_logout'),
    url('^reset-password/$', auth_views.password_reset, \
                                          name='auth_password_reset'),
    url('^reset-password/done/$', auth_views.password_reset_done, \
                                          name='password_reset_done'),
    url(r'^register/complete/$', RedirectView.as_view(pattern_name='home'),\
                                          name='registration_complete'),
    url(r'^users/', include('registration.backends.simple.urls',
                                               namespace='users')),

    # Social Auth Related urls
    url(r'^social/', include('social.apps.django_app.urls', namespace='social')),
    
    url(r'^admin/', admin.site.urls),
    url(r'^jsi18n\.js$', javascript_catalog , js_info_dict, name='javascript-catalog'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


