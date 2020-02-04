#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Student(models.Model):
    # Student Model

    class Meta(object):
        verbose_name = u"Стдент"
        verbose_name_plural = u"Студенти"

    first_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Ім'я"
    )

    last_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Прізвище"
    )

    middle_name = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=u"По-батькові",
        default=''
    )

    birthday = models.DateField(
        blank=False,
        verbose_name=u'Дата народження',
        null=True
    )

    photo = models.ImageField(
        blank=True,
        verbose_name=u"Фото",
        null=True
    )

    ticket = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Білет"
    )

    notes = models.TextField(
        max_length=256,
        blank=True,
        verbose_name=u"Додаткові нотатки"
    )

    student_group = models.ForeignKey('Group', 
        verbose_name=u"Група",
        blank=False,
        null=True,
        on_delete=models.PROTECT
        )

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)

class Exam(models.Model):
    # Exam Model

    class Meta(object):
        verbose_name = u"Іспит"
        verbose_name_plural = u"Іспити"

    title = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Назва предмету"
    )

    data_and_time = models.DataTimeField(
        auto_now=False, 
        auto_now_add=False,
        verbose_name=u"Дата"
    )

    teacher = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Викладач"
    )

    examenation = models.ManyToManyField('Group',
        max_length=256,
        blank=True,
        null=True,
        verbose_name=u"Складають іспит",
        on_delete=models.SET_NULL
    )
