import configparser
import pathlib


file_config = pathlib.Path(__file__).parent.joinpath('config.ini')
config = configparser.ConfigParser()
config.read(file_config)

username = config.get('DB', 'user')
password = config.get('DB', 'password')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

url = f'mongodb+srv://{username}:{password}@{domain}/{db_name}?retryWrites=true&w=majority'
