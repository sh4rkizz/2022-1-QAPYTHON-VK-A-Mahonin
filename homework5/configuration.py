import argparse
import json
import os

parser = argparse.ArgumentParser()
parser.add_argument(
    '--json',
    action='store_true',
)


def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


def report_result(header, output, file_to_write, add_keys_to_output=False):
    path = os.path.join(repo_root(), 'py_output')
    if not os.path.exists(path):
        os.makedirs(path)

    with open(os.path.join(path, f'{file_to_write}.txt'), 'w') as file:
        file.write(header + '\n')

        if parser.parse_args().json:
            file.write(json.dumps(str(output)))
        else:
            if isinstance(output, list):
                for i in output:
                    if add_keys_to_output:
                        file.write('\n'.join('\t'.join([k, str(i.get(k))]) for k in i.keys()))
                    else:
                        file.write('\t'.join(str(i.get(k)) for k in i.keys()))
                    file.write('\n')
            else:
                if add_keys_to_output:
                    file.write('\n'.join('\t'.join([k, str(output.get(k))]) for k in output.keys()))
                else:
                    file.write('\t'.join(str(output.get(k)) for k in output.keys()))
