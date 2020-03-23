from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from students.models.students_model import Student
from django.contrib.auth.models import User

def user_profile(request):
    import pdb;pdb.set_trace()
    persons = User.objects.all()
    students = Student.objects.all()
    
    return render(request, 'students/base.html', {'persons': persons, 'students': students})