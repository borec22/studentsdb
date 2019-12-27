# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse


#Views for groups    
def groups_list(request):
    groups = (
    {'id': 1,
    "name": 457,
    "starosta": u'Романчук Сергій',
    },
    {'id': 2,
    "name": 337,
    "starosta": u'Романчук Роман',
    }
    )
    return render (request,'students/list_group.html', {'groups': groups})
    
def groups_add(request):
    return HttpResponse('<h1> Group Add Form </h1>')
    
def gurnal(request):
    return HttpResponse('<h1> Yes zarabotalo! </h1>')    
    
def groups_edit(request, gid):
    return HttpResponse('<h1> Edit Group %s </h1>' % gid)
    
def groups_delete(request, gid):
    return HttpResponse('<h1> Delete Group %s </h1>'% gid)
