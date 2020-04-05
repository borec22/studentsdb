from django.core.management.base import BaseCommand

from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from students.models.students_model import Student
from students.models.groups_model import Group


class Command(BaseCommand):
    args = '<model_name model_name ...>'
    help = _(u"Prints to console number of student related objects in a database.")
    
    models = (('student', Student), ('group', Group), ('user', User))

    def handle(self, *args, **options):
    	for name, model in self.models:
    	    if name in args:
    		self.stdout.write(_(u'Number of %ss in database: %d') %
    			(name, model.objects.count()))

