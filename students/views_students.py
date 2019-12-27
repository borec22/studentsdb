# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

#Views for students 

def students_list(request):
	students = (
		{'id': 1,
		'first_name': u'Сергій',
		'last_name': u'Романчук',
		'ticket': 3,
		'image': 'img/me.jpg'},
		{'id': 2,
		 'first_name': u'Максим',
		 'last_name': u'Романчук',
		 'ticket': 6,
		 'image': 'img/max.jpg',
		},
		{'id': 3,
		 'image': 'img/podoba3.jpg',
		 'first_name': u'Віталій',
		 'last_name': u'Подоба',
		 'ticket': 9
		},	
	)
	
	return render(request,'students/students_list.html', {'students': students})
		
def students_add(request):
    return HttpResponse('<h1> Students Add Form </h1>')
    
def students_edit(request, sid):
    return HttpResponse('<h1> Edit student %s </h1>' % sid)
    
def students_delete(request, sid):
    return HttpResponse('<h1> Delete Student %s </h1>' % sid)
    



