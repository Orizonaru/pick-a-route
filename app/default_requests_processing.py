import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

class DefaultRequestsProcessing:
    def __init__(self, api_url, request_timeout=30):
        self.api_url = api_url
        self.http_session = requests.Session()
        self.request_timeout = request_timeout