import re
from collections import Counter
import configuration


def count_requests_with_server_error():
    regex = re.compile(r'\d+\.\d+\.\d+\..+[A-Z]{3,4} .+HTTP.+" 5.. \d+.+$', re.MULTILINE)

    with open(configuration.repo_root() + '/access.log', 'r') as file:
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
                'count': count
            } for ip_address, count in output[:5]
        ]

        configuration.report_result(
            header='Clients with the highest amount of failed requests (code 5xx)',
            output=output,
            file_to_write='count_server_based_errors'
        )


count_requests_with_server_error()
