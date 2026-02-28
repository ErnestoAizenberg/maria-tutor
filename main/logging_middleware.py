# core/middleware/logging_middleware.py
import logging
import time

logger = logging.getLogger('access')

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Логирование входящего запроса
        start_time = time.time()

        logger.info(
            "Incoming request",
            extra={
                'type': 'request_start',
                'path': request.path,
                'method': request.method,
                'user': request.user.username if request.user.is_authenticated else 'anonymous',
                'ip': request.META.get('REMOTE_ADDR'),
                'user_agent': request.META.get('HTTP_USER_AGENT', '')[:500]
            }
        )

        response = self.get_response(request)

        # Логирование завершения запроса
        duration = time.time() - start_time

        logger.info(
            "Request completed",
            extra={
                'type': 'request_end',
                'path': request.path,
                'method': request.method,
                'status_code': response.status_code,
                'duration': f"{duration:.3f}s",
                'user': request.user.username if request.user.is_authenticated else 'anonymous'
            }
        )

        return response
