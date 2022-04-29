import json
import logging
from socket import AF_INET, SOCK_STREAM, socket

from settings import MOCK_HOST, MOCK_PORT

logger = logging.getLogger('test_mock')


class HTTPClient:
    host = MOCK_HOST
    port = int(MOCK_PORT)

    def connect(self):
        logger.debug(f'Opening connection')
        socket_client = socket(
            AF_INET,
            SOCK_STREAM
        )
        socket_client.settimeout(0.5)
        socket_client.connect(
            (
                self.host,
                self.port
            )
        )
        return socket_client

    def post(self, params=None, data=None):
        params = f'/post_user/{params}'
        return self._request(method='POST', params=params, data=data)

    def get(self, params=None):
        params = f'/get_user/{params}'
        return self._request(method='GET', params=params)

    def put(self, params=None, data=None):
        params = f'/update_user/{params.get("name")}'
        return self._request(method='PUT', params=params, data=data)

    def delete(self, params=None, data=None):
        params = f'/delete_user/{params}'
        return self._request(method='DELETE', params=params, data=data, jsonify=True)

    def _request(self, method, params, data=None, jsonify=False):
        request = f'{method} {params} HTTP/1.1\r\nHost:{self.host}\r\n'

        request = request + '\r\n' if not jsonify \
            else request + f'Content-Type: application/json\r\n' \
                           f'Content-Length: {str(len(data))}\r\n\r\n' \
                           f'{json.dumps(data)}'

        socket_client = self.connect()

        socket_client.send(request.encode())

        logger.info(f'Sending request {request}')
        return self._receive(socket_client)

    def _receive(self, socket_client):
        total = []

        while True:
            data = socket_client.recv(2048)

            if data:
                logger.debug(f'Received data {data}')
                total.append(data.decode())
            else:
                logger.debug(f'Closing connection')
                socket_client.close()
                break

        return self._reformat_response(data)

    @staticmethod
    def _reformat_response(response):
        data = {'status_code': response[-1].split()[1]}

        headers = ''
        for elem in response:
            if elem:
                headers += elem + '\n'
            else:
                data['headers'] = headers
                break

        body = response[-1]
        data['body'] = body if not body else json.loads(body)

        return data
