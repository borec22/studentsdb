from .settings import PORTAL_URL
from students.util import get_groups, get_language_from_request

def students_proc(request):
	return {'PORTAL_URL': PORTAL_URL}

def groups_processor(request):
	return {'GROUPS': get_groups(request)}

def language_processor(request):
	return {'LANGUAGE': get_language_from_request(request)}

