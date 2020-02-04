# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from students.models.exams_model import Exam

#Views for groups  

def exam_list(request):
    exams = Exam.objects.all()
    #try to order exams list
    order_by = request.GET.get('order_by', '')
    if order_by in ('subject','teacher',):
        exams = exams.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            exams = exams.reverse()

    #paginate exams
    paginator = Paginator(exams, 2)
    page = request.GET.get('page', '')
    try:
        exams = paginator.page(page)
    except PageNotAnInteger:
        #If page is not an integer, deliver first page.
        exams = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver
        # last page of results
        exams = paginator.page(paginator.num_pages)
    return render (request, 'students/exam_list.html', {'exams': exams})

def exam_edit(request, eid):
    return HttpResponse('<h1> Edit exam %s </h1>' %eid)

def teacher_edit(request, tid):
    return HttpResponse('<h1> Edit teacher %s </h1>' %tid)

def add_exam(request):
    return HttpResponse('<h1> Add Exam </h1>')
      
