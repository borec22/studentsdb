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

from django.contrib import admin
from django.conf.urls import url, include

from django.views.generic import TemplateView
from .settings import MEDIA_ROOT, DEBUG
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Students urls
    url(r'^$', students_list, name='home'),
    url(r'^students/add/$', students_add, name='students_add'),
    url(r'^students/(?P<pk>\d+)/edit/$', StudentUpdateView.as_view(), name='students_edit'),
    url(r'^students/(?P<pk>\d+)/delete/$', StudentDeleteView.as_view(), name='students_delete'),
     
    #Groups urls
    url(r'^groups/$', groups_list, name='groups'),
    url(r'^groups/add/$', groups_add, name='groups_add'),  
    url(r'^groups/(?P<pk>\d+)/edit/$', GroupUpdateView.as_view(), name='groups_edit'),
    url(r'^groups/(?P<gid>\d+)/delete/$', GroupDeleteView, name='groups_delete'),
    

    #Journal urls
    url(r'^journal/(?P<pk>\d+)?/?$', JournalView.as_view(), name='journal'),

    #Exam urls
    url(r'^exam/$', exam_list, name='exam'),
    url(r'^exam/(?P<pk>\d+)/edit_exam/$', exam_edit.as_view(), name='exam_edit'),
    url(r'^exam/(?P<pk>\d+)/delete_exam/$', exam_delete.as_view(), name='exam_delete'),
    url(r'^exam/add/$', add_exam.as_view(), name='add_exam'),

    # Contact Admin Form
    url(r'^contact-admin/$', ContactAdminView.as_view(), name='contact_admin'),
    # Contact admin by help django application django-contact-form
    url(r'^django-contact-admin/$', CustomContactFormView.as_view(), name='django-contact-admin'),
    url(r'^contact/sent/$',
        TemplateView.as_view(
            template_name='contact_admin/django_contact_form_sent.html'
        ),
        name='contact_form_sent'),
    
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


