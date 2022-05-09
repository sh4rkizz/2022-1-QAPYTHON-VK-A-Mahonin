# Домашнее задание №5: Backend: Linux

#### Приведенные далее скрипты обрабатывают файл, находящийся в папке с домашней работой

## Общее количество запросов

*Bash скрипт*
```
#!/bin/bash
wc -l < access.log
```

*Описание работы*

Bash-скрипт осуществляет подсчет количества строк в файле access.log, которое равно количеству запросов 

*Вывод*
```
225133
```

*Python скрипт*
```
def count_requests():
    regex = re.compile(r'^.+$', re.MULTILINE)

    with open(configuration.repo_root() + '/access.log', 'r') as file:
        requests = re.findall(regex, file.read())

    configuration.report_result(
        header='Get overall request quantity over access.log',
        output={'count': len(requests)},
        file_to_write='count_requests'
    )
```

*Описание работы*

Python-скрипт осуществляет подсчет непустых строк в файле access.log, количество которых равно количеству запросов

*Файл вывода*
```
Get overall request quantity over access.log
225133
```

## Общее количество запросов по типу

*Bash скрипт*
```
#!/bin/bash
cat access.log | grep -Eo '(GET|POST|PUT|HEAD) ' | awk '{print $1}' | sort | uniq -c
```

*Описание работы*

Bash-скрипт осуществляет поиск строк с вхождением элемента группы (GET|POST|PUT|HEAD), после
чего выводит количество уникальных строк 

*Вывод*
```
 122096 GET
    529 HEAD
 102503 POST
      6 PUT
```

*Python скрипт*
```
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
```

*Описание работы*

Собственно, принцип работы не отличается от работы bash-скрипта, на каждое вхождение элемента
группы инкрементируется счетчик этого элемента в словаре

*Файл вывода*
```
Count all requests by type
POST	102504
GET	122095
HEAD	528
PUT	6
```

## Топ 10 самых частых запросов

*Bash скрипт*
```
#!/bin/bash
cat access.log | grep -Eo "[A-Z]{3,4}.+(HTTP)" | sed -r 's/\?.+//' | awk '{print $2}'|
 sort | uniq -c | sort -nr | head | awk '{print $1 "\t" $2}'
```

*Описание работы*

По регулярному выражению осуществляется поиск в файле, после чего выбирается второй
элемент найденной группы, по которому осуществляется дальнейший подсчет для каждого
типа url, после чего выводим 10 записей с помощью утилиты head

*Вывод*
```
103939  /administrator/index.php
26336   /apache-log/access.log
7682    /index.php
6981    /
4980    /templates/_system/css/general.css
3199    /robots.txt
2356    http://almhuette-raith.at/administrator/index.php
2201    /favicon.ico
1757    /wp-login.php
1563    /administrator/
```

*Python скрипт*
```
def most_frequent_requests():
    regex = re.compile(r'[A-Z]{3,4} .+$', re.MULTILINE)

    with open(configuration.repo_root() + '/access.log', 'r') as file:
        file = file.read()
        requests = [match.split()[1].split('?')[0] for match in re.findall(regex, file)]

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
            'count': count,
            'url': url
        } for url, count in output[:10]
    ]

    configuration.report_result(
        header='Top 10 most commonly requested urls',
        output=output,
        file_to_write='most_frequent_requests'
    )
```

*Описание работы*

По регулярному выражению осуществляется поиск в файле, после чего выбирается
второй элемент найденной группы, который становится ключом в словаре для осуществления подсчета

*Файл вывода*
```
Top 10 most commonly requested urls
103939	/administrator/index.php
26336	/apache-log/access.log
7682	/index.php
6981	/
4980	/templates/_system/css/general.css
3199	/robots.txt
2356	http://almhuette-raith.at/administrator/index.php
2201	/favicon.ico
1757	/wp-login.php
1563	/administrator/
```

## Топ 5 самых больших по размеру запросов, которые завершились клиентской (4ХХ) ошибкой

*Bash скрипт*
```
#!/bin/bash
cat access.log | grep -E "[A-Z]{3,4} .+(HTTP)" | awk '{print  $1 "\t" $9 "\t" $10 "\t" $7}'| awk '$2 ~/4../{print $0}' |
 awk '$0 = NR" "$0' | sort -k4rn -k1n | sed -r 's/\?.+//' | head -n 5 | awk '{$1=""; print $0}'
```

*Описание работы*

По регулярному выражению осуществляется поиск вхождения групп, после чего полученные строки сортируются
в обратном порядке по значению 3 столбца (размер запроса) и значению 1 столбца (номер строки в файле),
а вывод осуществляется параметризированной утилитой head

*Вывод*
```
189.217.45.73 404 1417 /index.php
189.217.45.73 404 1417 /index.php
189.217.45.73 404 1417 /index.php
189.217.45.73 404 1417 /index.php
104.129.9.248 404 1397 /index.php
```

*Python скрипт*
```
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
```

*Описание работы*

Принцип работы рзаключается в разбиении каждого совпадения по пробелам и записи в виде словаря
нужных данных в список запросов

*Файл вывода*
```
Top 5 biggest client based errors (code 4xx)
/index.php	404	1417	189.217.45.73
/index.php	404	1417	189.217.45.73
/index.php	404	1417	189.217.45.73
/index.php	404	1417	189.217.45.73
/index.php	404	1397	104.129.9.248
```

## Топ 5 пользователей по количеству запросов, которые завершились серверной (5ХХ) ошибкой

*Bash скрипт*
```
#!/bin/bash
cat access.log | grep -E "[A-Z]{3,} .+(HTTP)" | awk '$9~/5../{print $1}'| uniq -c| sort -nr |
 awk '{print $1 "\t" $2}' | head -n 5
```

*Описание работы*

Производится поиск всех запросов имеющих код ошибки 5хх и для них выводится первый столбец с помощью
awk, после чего подсчитывается количество запросов для уникальных ip-адресов, а полученные данные
сортируются в порядке убывания

*Вывод*
```
225     189.217.45.73
4       82.193.127.15
3       91.210.145.36
2       198.38.94.207
2       195.133.48.198
```

*Python скрипт*
```
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
```

*Описание работы*

Также как и ранее осуществляется поиск по регулярному выражению и после инвертированной
сортировки выводится пять первых элементов

*Файл вывода*
```
Clients with the highest amount of failed requests (code 5xx)
189.217.45.73	225
82.193.127.15	4
91.210.145.36	3
194.87.237.6	2
198.38.94.207	2
```

## Выводы по использованию скриптов

*Bash-скрипты*

Плюсы
* Обладают высоким быстродействием
* Занимают меньший объем
* Могут быть запущены из терминала

Минусы
* Сложность в написании команд

*Python-скрипты*

Плюсы
* Удобочитаемость кода
* Кроссплатформенность

Минусы
* Необходимость использования дополнительных библиотек
* Большой объем
