import configuration
import re


def count_requests_by_type():
    counter = {
        'POST': 0,
        'GET': 0,
        'HEAD': 0,
        'PUT': 0
    }

    regex = re.compile(
        '(GET|POST|PUT|HEAD) .+$',
        re.MULTILINE
    )

    with open(configuration.repo_root() + '/access.log', 'r') as file:
        all_occurrences = re.findall(regex, file.read())

        for match in all_occurrences:
            counter[f'{match.split()[0]}'] += 1

    configuration.report_result(
        header='Count all requests by type',
        output=counter,
        file_to_write='count_by_type',
        add_keys_to_output=True
    )


count_requests_by_type()
