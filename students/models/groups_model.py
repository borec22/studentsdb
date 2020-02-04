#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Group(models.Model):
    # Group Model

    class Meta(object):
        verbose_name = u"Група"
        verbose_name_plural = u"Групи"

    title = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Назва"
    )

    leader = models.OneToOneField('Student',
        max_length=256,
        blank=True,
        null=True,
        verbose_name=u"Староста",
        on_delete=models.SET_NULL
    )

    notes = models.TextField(
        max_length=256,
        blank=True,
        verbose_name=u"Додаткові нотатки"
    )

    def __unicode__(self):
        if self.leader:
            return u"%s %s %s" % (self.title, self.leader.first_name, self.leader.last_name)
        else:
            return u"%s" % (self.title)