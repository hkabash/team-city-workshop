import logging
import os
from http import HTTPStatus
from enums.host import BASE_URL

from swagger_coverage_py.configs import IS_DISABLED
from swagger_coverage_py.request_schema_handler import RequestSchemaHandler
from swagger_coverage_py.uri import URI


class CustomCoverageListener:
    def __init__(
            self,
            session,
            method,
            base_url,
            endpoint,
            uri_params,
            **kwargs
    ):
        self.__uri = URI(base_url, "", endpoint, **uri_params)
        self.response = session.request(method, self.__uri.full, **kwargs)
        if not IS_DISABLED:
            RequestSchemaHandler(
                self.__uri, method, self.response, kwargs
            ).write_schema()


class CustomRequester:
    base_headers = {"Content-Type": "application/json", "Accept": "application/json"}

    def __init__(self, session):
        self.session = session
        self.base_url = BASE_URL
        self.logger = logging.getLogger(__name__)

    def send_request(self, method, endpoint, data=None, expected_status=HTTPStatus.OK, need_logging=True):
        """
        Враппер для запросов. Позволяет добовлять различную логику
        :param method: Метод запроса
        :param endpoint: Эндпоинт для склейки с BASE_URL в переменной "url"
        :param data: Тело запроса. По умолчанию пустое, чтобы пропускало NO_CONTENT ответы
        :param expected_status: Ожидаемый статус ответа.
        :param need_logging: Передача флага для логгирования. По умолчанию = True
        :return: Возвращает объект ответа
        """
        # url = f"{self.base_url}{endpoint}"

        # Prepare kwargs for CoverageListener, similar to what you would pass to requests.request
        request_kwargs = {
            "json": data,
            # Include any other kwargs you would normally pass to requests.request
        }

        # Instantiate CoverageListener, which will make the request and track it for Swagger coverage
        coverage_listener = CustomCoverageListener(
            session=self.session,
            method=method,
            base_url=self.base_url,
            endpoint=endpoint,
            uri_params={},
            **request_kwargs,
        )

        response = coverage_listener.response

        # response = self.session.request(method, url, json=data)
        if need_logging:
            self.log_request_and_response(response)
        if response.status_code != expected_status:
            raise ValueError(f"Unexpected status code: {response.status_code}")
        return response

    def _update_session_headers(self, **kwargs):
        self.headers = self.base_headers.copy()
        self.headers.update(kwargs)
        self.session.headers.update(self.headers)

    def log_request_and_response(self, response):
        """
        Логгирование запросов и ответов. Настройки логгирования описаны в pytest.ini
        Преобразует вывод в curl-like (-H хэдеры), (-d тело)

        :param response: Объект response получаемый из метода "send_request"
        """
        try:
            request = response.request
            GREEN = '\033[32m'
            RED = '\033[31m'
            RESET = '\033[0m'
            headers = " \\\n".join([f"-H '{header}: {value}'" for header, value in request.headers.items()])

            full_test_name = f"pytest {os.environ.get('PYTEST_CURRENT_TEST', '').replace(' (call)', '')}"

            body = ""
            if hasattr(request, 'body') and request.body is not None:
                if isinstance(request.body, bytes):
                    body = request.body.decode('utf-8')
            body = f"-d '{body}' \n" if body != "{}" else ""

            self.logger.info(
                f"{GREEN}{full_test_name}{RESET}\n"
                f"curl -X {request.method} '{request.url}' \\\n"
                f"{headers} \\\n"
                f"{body}"
            )

            response_status = response.status_code
            response_is_successful = response.ok
            response_data = response.text

            if not response_is_successful:
                self.logger.info(f"\tRESPONSE:"
                                 f"\nSTATUS_CODE: {RED}{response_status}{RESET}"
                                 f"\nDATA: {RED}{response_data}{RESET}")
        except Exception as e:
            self.logger.info(f"\nLogging went wrong: {type(e)} - {e}")
