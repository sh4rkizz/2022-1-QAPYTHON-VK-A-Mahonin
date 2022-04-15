import configuration

import re


def count_requests():
    regex = re.compile(r'^.+$', re.MULTILINE)

    with open(configuration.repo_root() + '/access.log', 'r') as file:
        requests = re.findall(regex, file.read())

    configuration.report_result(
        header='Get overall request quantity over access.log',
        output={'count': len(requests)},
        file_to_write='count_requests'
    )


count_requests()
