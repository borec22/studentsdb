#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Exam(models.Model):
    # Exam Model

    class Meta(object):
        verbose_name = u"Іспит"
        verbose_name_plural = u"Іспити"

    subject = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Назва предмету"
    )

    data_and_time = models.DateTimeField(
        blank=False,
        null=True,
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
        verbose_name=u"Складають іспит"
    )

    def __unicode__(self):
        return u"%s " %(self.subject)