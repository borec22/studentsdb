# _*_ coding: utf-8 _*_
from django.db import models

class MonthJournal(models.Model):
    """Student Monthly Journal"""

    class Meta:
        verbose_name = u'Місячний Журнал'
        verbose_name_plural = u'Місячні Журнали'

    student = models.ForeignKey('Student',
        verbose_name=u'Студент',
        blank=False,
        unique_for_month='date')

    # we only need year and month, so always set day first day of the month
    date = models.DateField(
    	verbose_name=u'Дата',
    	blank=False)

    # list of days, each says wheher student was presene or not
    scope = locals()
    for fields_number in range(1, 32):
        scope['present_day' + str(fields_number)] = models.BooleanField(\
    		verbose_name=u'День №' + str(fields_number), 
    		default=False)

    def __unicode__(self):
    	return u'%s: %d, %d' %(self.student.last_name, self.date.month, self.date.year)