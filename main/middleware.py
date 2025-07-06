# middleware.py
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template import TemplateDoesNotExist
import logging
from tutorproject.logger import setup_logger

logger = setup_logger(log_file="app.log", level="DEBUG")

class CustomErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logger.debug("CustomErrorMiddleware initialized")

    def __call__(self, request):
        logger.info(f"Incoming request: {request.method} {request.path}")
        logger.debug(f"Request headers: {request.headers}")
        logger.debug(f"Request GET params: {request.GET}")
        logger.debug(f"Request POST data: {request.POST}")

        try:
            response = self.get_response(request)
            logger.debug(f"Response status: {response.status_code}")
            logger.debug(f"Response headers: {response.headers}")

            # Обрабатываем HTTP-коды ошибок
            if 400 <= response.status_code < 600:
                logger.warning(f"Error response detected: {response.status_code} for {request.path}")
                return self.render_error_page(request, response.status_code)

            return response
        except Exception as e:
            logger.error(f"Unhandled exception in middleware: {str(e)}", exc_info=True)
            raise

    def process_exception(self, request, exception):
        # Получаем код статуса из исключения или используем 500 по умолчанию
        status_code = getattr(exception, 'status_code', 500)
        logger.error(
            f"Exception occurred: {str(exception)} (status: {status_code})",
            exc_info=True,
            extra={
                'request_path': request.path,
                'request_method': request.method,
                'exception_type': type(exception).__name__
            }
        )
        return self.render_error_page(request, status_code, exception)

    def render_error_page(self, request, status_code, exception=None):
        template_name = f'errors/{status_code}.html'
        context = {
            'status_code': status_code,
            'exception': str(exception) if exception else None,
            'request_path': request.path
        }

        logger.info(
            f"Rendering error page for status {status_code}",
            extra={
                'template_name': template_name,
                'exception': str(exception) if exception else None,
                'request_path': request.path
            }
        )

        try:
            html_content = render_to_string(template_name, context)
            logger.debug(f"Successfully rendered error template: {template_name}")
            return HttpResponse(
                html_content,
                status=status_code,
                content_type='text/html'
            )
        except TemplateDoesNotExist:
            logger.warning(f"Error template not found: {template_name}. Falling back to plain text response.")
            # Если шаблона нет - возвращаем минимальный ответ
            return HttpResponse(
                f"Error {status_code}",
                status=status_code,
                content_type='text/plain'
            )
        except Exception as e:
            logger.critical(
                f"Failed to render error page for status {status_code}: {str(e)}",
                exc_info=True
            )
            # Fallback response if even the plain text rendering fails
            return HttpResponse(
                "Internal Server Error",
                status=500,
                content_type='text/plain'
            )
