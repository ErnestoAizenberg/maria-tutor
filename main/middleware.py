import logging

from django.http import HttpResponse
from django.template import TemplateDoesNotExist
from django.template.response import TemplateResponse


class CustomErrorMiddleware:
    def __init__(self, get_response):
        self.logger = logging.getLogger("django.request")
        self.get_response = get_response
        self.logger.debug("CustomErrorMiddleware initialized")

    def __call__(self, request):
        self.logger.info(f"Incoming request: {request.method} {request.path}")
        self.logger.debug(f"Request headers: {request.headers}")
        self.logger.debug(f"Request GET params: {request.GET}")
        self.logger.debug(f"Request POST data: {request.POST}")

        try:
            response = self.get_response(request)
            self.logger.debug(f"Response status: {response.status_code}")
            self.logger.debug(f"Response headers: {response.headers}")

            # Обрабатываем HTTP-коды ошибок
            if 400 <= response.status_code < 600:
                self.logger.warning(
                    f"Error response detected: {response.status_code} for {request.path}"
                )
                return self.render_error_page(request, response.status_code)

            return response
        except Exception as e:
            self.logger.error(
                f"Unhandled exception in middleware: {str(e)}", exc_info=True
            )
            raise

    def process_exception(self, request, exception):
        # Получаем код статуса из исключения или используем 500 по умолчанию
        status_code = getattr(exception, "status_code", 500)
        self.logger.error(
            f"Exception occurred: {str(exception)} (status: {status_code})",
            exc_info=True,
            extra={
                "request_path": request.path,
                "request_method": request.method,
                "exception_type": type(exception).__name__,
            },
        )
        return self.render_error_page(request, status_code, exception)

    def render_error_page(self, request, status_code, exception=None):
        template_name = f"errors/{status_code}.html"
        context = {
            "status_code": status_code,
            "exception": str(exception) if exception else None,
            "request_path": request.path,
        }

        self.logger.info(
            f"Rendering error page for status {status_code}",
            extra={
                "template_name": template_name,
                "exception": str(exception) if exception else None,
                "request_path": request.path,
            },
        )

        try:
            response = TemplateResponse(
                request, template_name, context, status=status_code
            )
            response.render()
            self.logger.debug(f"Successfully rendered error template: {template_name}")
            return response
        except TemplateDoesNotExist:
            self.logger.warning(
                f"Error template not found: {template_name}. Falling back to plain text response."
            )
            # Если шаблона нет - возвращаем минимальный ответ
            return HttpResponse(
                f"Error {status_code}", status=status_code, content_type="text/plain"
            )
        except Exception as e:
            self.logger.critical(
                f"Failed to render error page for status {status_code}: {str(e)}",
                exc_info=True,
            )
            # Fallback response if even the plain text rendering fails
            return HttpResponse(
                "Internal Server Error", status=500, content_type="text/plain"
            )
