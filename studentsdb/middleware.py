from datetime import datetime

from django.http import HttpResponse
from .settings import DEBUG
from bs4 import BeautifulSoup


class RequestTimeMiddleware(object):
    """Display request time on a page"""

    def process_request(self, request):
        request.start_time = datetime.now()
        return None

    def process_response(self, request, response):
		# if our process_request was canceled somewhere whithin
		# middleware stack, we can not calculate request time
        if not hasattr(request, 'start_time'):
            return response

		# calculate request execution time
        request.end_time = datetime.now()
        time_delta = (request.end_time - request.start_time)
        if 'text/html' in response.get('Content-Type', '') and DEBUG:
            if time_delta.seconds < 2:
                soup = BeautifulSoup(response.content, 'lxml')
                if soup.body:
                    time_measure_tag = soup.new_tag('code', id="time-middleware", 
                	style="margin-left: 100px;")
                    time_measure_tag.append('Request took: %s' %str(time_delta))
                    soup.body.insert(0, time_measure_tag)
                    response.content = soup.prettify(soup.original_encoding)

        return response

	def process_view(self, request, view, args, kwargs):
		return None

	def process_template_response(self, request, response):
		return response

	def process_exception(self, request, exception):
		return HttpResponse('Exception found: %s' % exception)
