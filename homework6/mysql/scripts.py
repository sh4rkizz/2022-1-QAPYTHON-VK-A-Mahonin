import re
from collections import Counter

from conftest import repo_root
from mysql.models import AllRequests, \
    RequestsByType, \
    TheMostFrequentRequests, \
    ClientBasedErrors, \
    ServerBasedErrors


class LogBuilder:
    def __init__(self, client):
        self.client = client
        self.file_path = repo_root() + '/access.log'

    def count_requests(self):
        regex = re.compile(r'^.+$', re.MULTILINE)

        with open(self.file_path, 'r') as file:
            output = re.findall(regex, file.read())

        self.client.session.add(
            AllRequests(quantity=len(output))
        )

    def count_requests_by_type(self) -> int:
        line_counter = 0
        output = {
            'POST': 0,
            'GET': 0,
            'HEAD': 0,
            'PUT': 0
        }

        regex = re.compile(
            '(GET|POST|PUT|HEAD) .+$',
            re.MULTILINE
        )

        with open(self.file_path, 'r') as file:
            matches = re.findall(regex, file.read())

        for match in matches:
            output[f'{match.split()[0]}'] += 1

        for line_counter, (request_type, quantity) in enumerate(output.items(), start=1):
            self.client.session.add(
                RequestsByType(
                    type=request_type,
                    quantity=quantity
                )
            )

        return line_counter

    def count_most_frequent_requests(self) -> int:
        line_counter = 0
        regex = re.compile(r'[A-Z]{3,4} .+$', re.MULTILINE)

        with open(self.file_path, 'r') as file:
            file = file.read()
            requests = [match.split()[1] for match in re.findall(regex, file)]

        requests.sort()
        output = list(
            zip(
                Counter(requests).keys(),
                Counter(requests).values()
            )
        )

        output.sort(key=lambda elem: elem[1], reverse=True)
        output = [
            {
                'url': url,
                'quantity': quantity
            } for url, quantity in output[:10]
        ]

        for line_counter, out_elem in enumerate(output, start=1):
            self.client.session.add(
                TheMostFrequentRequests(
                    url=out_elem.get('url'),
                    quantity=out_elem.get('quantity')
                )
            )

        return line_counter

    def count_biggest_client_based_errors(self) -> int:
        line_counter = 0
        regex = re.compile(r'\d+\.\d+\.\d+\..+[A-Z]{3,4} .+HTTP.+" 4.. \d+', re.MULTILINE)

        with open(self.file_path, 'r') as file:
            output = [
                {
                    'url': match.split()[6],
                    'status_code': match.split()[8],
                    'size': int(match.split()[9]),
                    'ip': match.split()[0],
                } for match in re.findall(regex, file.read())
            ]

        output.sort(
            key=lambda elem: elem.get('size'),
            reverse=True
        )

        output = output[:5]
        for line_counter, out_elem in enumerate(output, start=1):
            self.client.session.add(
                ClientBasedErrors(
                    url=out_elem.get('url'),
                    size=out_elem.get('size'),
                    ip_address=out_elem.get('ip'),
                    status_code=out_elem.get('status_code')
                )
            )

        return line_counter

    def count_requests_with_server_error(self) -> int:
        line_counter = 0
        regex = re.compile(r'\d+\.\d+\.\d+\..+[A-Z]{3,4} .+HTTP.+" 5.. \d+.+$', re.MULTILINE)

        with open(self.file_path, 'r') as file:
            ip = [match.split()[0] for match in re.findall(regex, file.read())]

        output = list(
            zip(
                Counter(ip).keys(),
                Counter(ip).values()
            )
        )

        output.sort(
            key=lambda elem: elem[1],
            reverse=True
        )

        output = [
            {
                'ip_address': ip_address,
                'quantity': quantity
            } for ip_address, quantity in output[:5]
        ]

        for line_counter, out_elem in enumerate(output, start=1):
            self.client.session.add(
                ServerBasedErrors(
                    ip_address=out_elem.get('ip_address'),
                    quantity=out_elem.get('quantity'),
                )
            )

        return line_counter
