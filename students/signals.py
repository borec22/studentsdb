# _*_ codding: utf-8 _*_
import logging

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from students.models import Student, Group, Exam


# procesing signals in Student
@receiver(post_save)
def log_student_updated_added_event(sender, **kwargs):
    """Writes information about newly added or updated student 
       into log file"""
    logger = logging.getLogger(__name__)

    group = kwargs['instance']
    if sender == Student:
        student = kwargs['instance']
        if kwargs['created']:
    	    logger.info("Student added: %s %s (ID: %d)", student.first_name,\
    		         student.last_name, student.id)
        else:
    	    logger.info("Student updated: %s %s (ID: %d)", student.first_name,\
    		         student.last_name, student.id)
    elif sender == Group:
    	group = kwargs['instance']
        if kwargs['created']:
    	    logger.info("Group added: %s (ID: %d)", group.title,\
    		         group.id)
        else:
    	    logger.info("Group updated: %s (ID: %d)", group.title,\
    		         group.id)
    else:
    	exam = kwargs['instance']
        if kwargs['created']:
    	    logger.info("Exam added: %s (ID: %d)", exam.subject,\
    		         exam.id)
        else:
    	    logger.info("Exam updated: %s (ID: %d)", exam.subject,\
    		         exam.id)

@receiver(post_delete)
def log_student_deleted_event(sender, **kwargs):
    """Writes information about deleted student into log file"""
    logger = logging.getLogger(__name__)
    
    if sender==Student:
        student = kwargs['instance']
        logger.info("Student delete: %s %s (ID: %d)", student.first_name,\
    	    student.last_name, student.id)

    elif sender==Group:
        group = kwargs['instance']
        logger.info("Group delete: %s (ID: %d)", group.title,\
    		         group.id)
    else:
    	exam = kwargs['instance']
        logger.info("Exam delete: %s (ID: %d)", exam.subject,\
    		         exam.id)


