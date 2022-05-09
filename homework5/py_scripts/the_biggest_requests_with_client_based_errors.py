import configuration
import re


def biggest_client_based_errors():
    regex = re.compile(r'\d+\.\d+\.\d+\..+[A-Z]{3,4} .+HTTP.+" 4.. \d+', re.MULTILINE)

    with open(configuration.repo_root() + '/access.log', 'r') as file:
        output = [
            {
                'url': match.split()[6].split('?')[0],
                'status_code': match.split()[8],
                'size': int(match.split()[9]),
                'ip': match.split()[0],
                'pos': enum,
            } for enum, match in enumerate(re.findall(regex, file.read()))
        ]

        # sort by size and file order
        output = list(
            sorted(
                output,
                key=lambda elem: (elem['size'], -elem['pos']),
                reverse=True
            )
        )[:5]

        for x in output:
            x.pop('pos')

        configuration.report_result(
            header='Top 5 biggest client based errors (code 4xx)',
            output=output[:5],
            file_to_write='biggest_client_based_errors'
        )


biggest_client_based_errors()
