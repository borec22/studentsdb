#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.db import models


class Exam(models.Model):
    # Exam Model

    class Meta(object):
        verbose_name = _(u"Exam")
        verbose_name_plural = _(u"Exams")

    subject = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_(u"Subject")
    )

    data = models.DateField(
        blank=False,
        null=True,
        verbose_name=_(u"Data")
    )

    teacher = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_(u"Teacher")
    )

    examenation = models.ManyToManyField('Group',
        max_length=256,
        blank=True,
        verbose_name=_(u"Take of exam")
    )

    def __unicode__(self):
        return u"%s " %(self.subject)