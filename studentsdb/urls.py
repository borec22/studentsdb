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

from django.contrib import admin
from django.conf.urls import url, include
from .settings import MEDIA_ROOT, DEBUG
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Students urls
    url(r'^$', students_list, name='home'),
    url(r'^students/add/$', students_add, name='students_add'),
    url(r'^students/(?P<sid>\d+)/edit/$', students_edit, name='students_edit'),
    url(r'^students/(?P<sid>\d+)/delete/$', students_delete, name='students_delete'),
     
    #Groups urls
    url(r'^groups/$', groups_list, name='groups'),
    url(r'^groups/add/$', groups_add, name='groups_add'),  
    url(r'^groups/(?P<gid>\d+)/edit/$', groups_edit, name='groups_edit'),
    url(r'^groups/(?P<gid>\d+)/delete/$', groups_delete, name='groups_delete'),
    

    #Journal urls
    url(r'^journal/$', journal_list, name='journal'),

    #Exam urls
    url(r'^exam/$', exam_list, name='exam'),
    url(r'^exam/(?P<eid>\d+)/edit_exam/$', exam_edit, name='exam_edit'),
    url(r'^exam/(?P<tid>\d+)/edit_teacher/$', teacher_edit, name='teacher_edit'),
    url(r'^exam/add/$', add_exam, name='add_exam'),
    
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


