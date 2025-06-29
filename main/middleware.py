# middleware.py
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template import TemplateDoesNotExist

class CustomErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Обрабатываем HTTP-коды ошибок
        if 400 <= response.status_code < 600:
            return self.render_error_page(request, response.status_code)
        return response

    def process_exception(self, request, exception):
        # Получаем код статуса из исключения или используем 500 по умолчанию
        status_code = getattr(exception, 'status_code', 500)
        return self.render_error_page(request, status_code, exception)

    def render_error_page(self, request, status_code, exception=None):
        template_name = f'errors/{status_code}.html'
        context = {
            'status_code': status_code,
            'exception': str(exception) if exception else None,
            'request_path': request.path
        }

        try:
            return HttpResponse(
                render_to_string(template_name, context),
                status=status_code,
                content_type='text/html'
            )
        except TemplateDoesNotExist:
            # Если шаблона нет - возвращаем минимальный ответ
            return HttpResponse(
                f"Error {status_code}",
                status=status_code,
                content_type='text/plain'
            )
