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
        output = dict()

        regex = re.compile(
            '\"([A-Z]{3,7}) .+$',
            re.MULTILINE
        )

        with open(self.file_path, 'r') as file:
            matches = re.findall(regex, file.read())

        for match in matches:
            elem = f'{match}'

            if output.get(elem) is None:
                output.setdefault(elem, 0)

            output[elem] += 1

        for line_counter, (request_type, quantity) in enumerate(output.items(), start=1):
            self.client.session.add(
                RequestsByType(
                    type=request_type,
                    quantity=quantity
                )
            )

        return line_counter

    def count_most_frequent_requests(self, length=10) -> int:
        line_counter = 0
        regex = re.compile(r'[A-Z]{3,7} .+$', re.MULTILINE)

        with open(self.file_path, 'r') as file:
            requests = [match.split()[1].split('?')[0] for match in re.findall(regex, file.read())]

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
                'quantity': quantity,
                'url': url
            } for url, quantity in output[:length]
        ]

        for line_counter, out_elem in enumerate(output, start=1):
            self.client.session.add(
                TheMostFrequentRequests(
                    url=out_elem.get('url'),
                    quantity=out_elem.get('quantity')
                )
            )

        return line_counter

    def count_biggest_client_based_errors(self, length=5) -> int:
        line_counter = 0
        regex = re.compile(r'\d+\.\d+\.\d+\..+[A-Z]{3,7} .+HTTP.+" 4.. \d+', re.MULTILINE)

        with open(self.file_path, 'r') as file:
            output = [
                {
                    'url': match.split()[6].split('?')[0],
                    'status_code': match.split()[8],
                    'size': int(match.split()[9]),
                    'ip': match.split()[0],
                    'pos': enum,
                } for enum, match in enumerate(re.findall(regex, file.read()))
            ]

        output = list(
            sorted(
                output,
                key=lambda elem: (elem['size'], -elem['pos']),
                reverse=True
            )
        )[:length]

        for x in output:
            x.pop('pos')

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

    def count_requests_with_server_error(self, length=5) -> int:
        line_counter = 0
        regex = re.compile(r'\d+\.\d+\.\d+\..+[A-Z]{3,7} .+HTTP.+" 5.. \d+.+$', re.MULTILINE)

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
            } for ip_address, quantity in output[:length]
        ]

        for line_counter, out_elem in enumerate(output, start=1):
            self.client.session.add(
                ServerBasedErrors(
                    ip_address=out_elem.get('ip_address'),
                    quantity=out_elem.get('quantity'),
                )
            )

        return line_counter
