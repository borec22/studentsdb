# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.core.urlresolvers import reverse
from .models import Student
from .models import Group
from .models import Exam, MonthJournal

from django.forms import ModelForm, ValidationError

class StudentFormAdmin(ModelForm):
    
    def clean_student_group(self):
        """Check if student is leader in any group.

        If yes, then ensure it's the same as selected group."""
        # get group where current student is a leader
        groups = Group.objects.filter(leader=self.instance)
        if len(groups) > 0 and self.cleaned_data['student_group'] != groups[0]:
            raise ValidationError(u'Студент є старостою іншої групи.', code='invalid')
        return self.cleaned_data['student_group']

class StudentAdmin(admin.ModelAdmin):
	list_display = ['last_name', 'first_name', 'ticket', 'student_group']
	list_display_links = ['last_name', 'first_name']
	ordering = ['last_name']
	list_filter = ['student_group']
	list_editable = ['student_group']
	list_per_page = 5
	search_fields = ['last_name', 'first_name', 'middle_name', 'ticket', 'notes']
	form = StudentFormAdmin

	def view_on_site(self, obj):
		return reverse('students_edit', kwargs={'pk': obj.id})

class GroupFormAdmin(ModelForm):
    
    def clean(self):
    	group = Group.objects.filter(title=self.cleaned_data['title'])
    	if  len(group) > 1:
    		raise ValidationError('Така група вже існує.', code='invalid')


class GroupAdmin(admin.ModelAdmin):
	list_display = ['title', 'leader']
	list_display_links = ['title', 'leader']
	ordering = ['title']
	list_filter = ['title']
	list_per_page = 5
	search_fields = ['title']
	
	form = GroupFormAdmin

	def view_on_site(self, obj):
		return reverse('groups_edit', kwargs={'gid': obj.id})

class ExamAdmin(admin.ModelAdmin):
	list_display = ['subject', 'data', 'teacher']
	list_display_links = ['subject', 'data']
	ordering = ['subject']
	list_filter = ['subject']
	lisp_per_page = 5
	search_fields = ['subject']

	def view_on_site(self, obj):
		return reverse('exam_edit', kwargs={'pk': obj.id})

# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(MonthJournal)




