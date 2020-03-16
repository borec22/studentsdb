#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.db import models


class Group(models.Model):
    # Group Model

    class Meta(object):
        verbose_name = _(u"Group")
        verbose_name_plural = _(u"Groups")

    title = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_(u"Title")
    )

    leader = models.OneToOneField('Student',
        max_length=256,
        blank=False,
        null=True,
        verbose_name=_(u"Leader"),
        on_delete=models.SET_NULL
    )

    notes = models.TextField(
        max_length=256,
        blank=True,
        verbose_name=_(u"Extra notes")
    )

    def __unicode__(self):
        if self.leader:
            return u"%s %s %s" % (self.title, self.leader.first_name, self.leader.last_name)
        else:
            return u"%s" % (self.title)