import configuration
import re


def biggest_client_based_errors():
    regex = re.compile(r'\d+\.\d+\.\d+\..+[A-Z]{3,4} .+HTTP.+" 4.. \d+', re.MULTILINE)

    with open(configuration.repo_root() + '/access.log', 'r') as file:
        output = [
            {
                'url': match.split()[6],
                'status_code': match.split()[8],
                'size': int(match.split()[9]),
                'ip': match.split()[0],
            } for match in re.findall(regex, file.read())
        ]

        output.sort(
            key=lambda o: o['size'],
            reverse=True
        )

        configuration.report_result(
            header='Top 5 biggest client based errors (code 4xx)',
            output=output[:5],
            file_to_write='biggest_client_based_errors'
        )


biggest_client_based_errors()
