import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

class DefaultRequestsProcessing:
    def __init__(self, api_url, request_timeout=30):
        self.api_url = api_url
        self.http_session = requests.Session()
        self.request_timeout = request_timeout

    def _construct_url(self, endpoint):
        return f"{self.api_url}/{endpoint}"

    def fetch(self, endpoint, query_params=None, request_headers=None):
        full_url = self._construct_url(endpoint)
        log.info(f"Отправка GET-запроса на {full_url} с параметрами: {query_params} и заголовками: {request_headers}")
        try:
            response = self.http_session.get(full_url, params=query_params, headers=request_headers, timeout=self.request_timeout)
            self._process_response(response)
            log.info(f"GET-запрос на {full_url} выполнен успешно. Статус: {response.status_code}")
            return response.json()
        except Exception as error:
            log.error(f"Ошибка при выполнении GET-запроса на {full_url}: {error}")
            raise

    def send(self, resource, payload=None, request_headers=None):
        full_url = self._construct_url(resource)
        log.info(f"Отправка POST-запроса на {full_url} с данными: {payload} и заголовками: {request_headers}")
        try:
            response = self.http_session.post(full_url, json=payload, headers=request_headers, timeout=self.request_timeout)
            self._process_response(response)
            log.info(f"POST-запрос на {full_url} выполнен успешно. Статус: {response.status_code}")
            return response.json()
        except Exception as error:
            log.error(f"Ошибка при выполнении POST-запроса на {full_url}: {error}")
            raise

    def _process_response(self, response):
        if response.ok:
            log.debug(f"Успешный ответ: {response.status_code} - {response.text}")
        else:
            log.error(f"Ошибка API: {response.status_code} - {response.text}")
            raise Exception(f"Ошибка API: {response.status_code} - {response.text}")