import configparser


class Constants:

    __CONFIG_FILE = 'secrets.ini'
    __config = configparser.ConfigParser()
    __config.read(__CONFIG_FILE)

    GOOGLE_CLOUD_API_KEY = __config['api-key']['google_cloud']
    GOOGLE_CLOUD_API_VERSION = 'v3'
    GOOGLE_CLOUD_SERVICE_NAME = 'youtube'


