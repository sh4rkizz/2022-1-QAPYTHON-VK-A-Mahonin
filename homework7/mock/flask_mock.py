import json
import logging
import threading

import requests
from flask import Flask, jsonify, request

from settings import MOCK_URL, MOCK_HOST, MOCK_PORT

logger = logging.getLogger('test_mock')

app = Flask(__name__)
DATA = {}


@app.route('/post_user', methods=['POST'])
def post_user():
    name = json.loads(request.data)['name']
    logger.debug(f'Trying to create a user {name}')

    if name in DATA:
        logger.error(f'The user {name} was not created', 400)
        return jsonify(f'User {name} already exists or other problem occurred'), 400

    DATA[name] = json.loads(request.data)['surname']

    logger.info(f'New user {name} {DATA[name]} was created')
    return jsonify(DATA[name]), 201


@app.route('/get_user/<name>', methods=['GET'])
def get_user_last_name(name):
    logger.debug(f'Trying to find a user {name}')

    if name not in DATA:
        logger.error(f'The user {name} was not found', 404)
        return jsonify({'msg': f'The user {name} was not found'}), 404

    logger.debug(f'User {name} {DATA[name]} was found')
    return jsonify(DATA.get(name)), 200


@app.route('/update_user/<name>', methods=['PUT'])
def update_user(name):
    if name not in DATA:
        logger.error(f'The user {name} was not found', 404)
        return jsonify({'msg': f'The user {name} was not found'}), 404

    surname = json.loads(request.data)[f'{name}']
    DATA.update({name: surname})

    logger.debug(f'Updating {name} with {surname}', 202)
    return jsonify(surname), 202


@app.route('/delete_user/<name>', methods=['DELETE'])
def delete_user(name):
    if name not in DATA:
        logger.error(f'The user {name} was not found', 404)
        return jsonify(f'Surname for user {name} not found'), 404

    DATA.pop(name)
    logger.debug(f'User {name} was deleted', 204)
    return jsonify(f'User {name} was deleted'), 204


@app.route('/users/all', methods=['GET'])
def get_all_users():
    if not DATA:
        logger.error(f'Empty response', 204)
        return jsonify(f'Empty response'), 204

    logger.debug(f'Userlist reached successfully')
    return jsonify(DATA)


def mock_run():
    server = threading.Thread(
        target=app.run,
        kwargs={
            'host': MOCK_HOST,
            'port': int(MOCK_PORT)
        }
    )

    server.start()
    logger.info('Mock server is starting')

    return server


def mock_stop():
    logger.info('Mock server was stopped')
    requests.get(MOCK_URL + '/shutdown')


@app.route('/shutdown')
def mock_shutdown():
    terminate = request.environ.get('werkzeug.server.shutdown')
    if terminate:
        terminate()
        logger.info('Mock server was terminated')

    return jsonify(f'OK, exiting'), 200
