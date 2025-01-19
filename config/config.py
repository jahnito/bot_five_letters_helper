import json


__all__ = ['Config']


class Config():
    def __init__(self):
        cfg = read_config_file()
        self.token = cfg['bot_token']
        self.db = cfg['db']


def read_config_file(config_file: str = 'config/config.json'):
    with open(config_file, 'r') as conf:
        data = json.load(conf)
    return data


if __name__ == '__main__':
    config = Config()
    print(config.token)
    print(config.db)