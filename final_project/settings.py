class AppSettings:
    APP_HOST = '0.0.0.0'
    APP_PORT = 8080

    APP_URL = f'{APP_HOST}:{APP_PORT}'


class MySqlSettings(AppSettings):
    MYSQL_HOST = '127.0.0.1'
    MYSQL_PORT = 3306
    DATABASE = 'vkeducation'

    DB_URL = f'mysql://{MYSQL_HOST}:{MYSQL_PORT}/{DATABASE}'


class VkApiSettings(AppSettings):
    VK_API_HOST = 'vk_api'
    VK_API_PORT = 8090

    VK_URL = f'{VK_API_HOST}:{VK_API_PORT}'


class JenkinsSettings(AppSettings):
    JKS_PORT = 8085


class StatusCode:
    SUCCESS = 200
    CREATED = 201
    NO_CONTENT = 204
    BUGGED_CREATED = 210

    NOT_CHANGED = 304

    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404

    INTERNAL_ERROR = 500

    BLOCKED = INACTIVE = 0
    UNBLOCKED = ACTIVE = 1
