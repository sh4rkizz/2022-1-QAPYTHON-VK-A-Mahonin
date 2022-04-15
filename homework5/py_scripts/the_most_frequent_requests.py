import re
from collections import Counter
import configuration


def most_frequent_requests():
    regex = re.compile(r'[A-Z]{3,4} .+$', re.MULTILINE)

    with open(configuration.repo_root() + '/access.log', 'r') as file:
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
            'count': count
        } for url, count in output[:10]
    ]

    configuration.report_result(
        header='Top 10 most commonly requested urls',
        output=output,
        file_to_write='most_frequent_requests'
    )


most_frequent_requests()
