import configparser

CONFIG_FILE = 'config.ini'

config = configparser.ConfigParser()
config.read(CONFIG_FILE)
print(config['api-key']['google_cloud'])
