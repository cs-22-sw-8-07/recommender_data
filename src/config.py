import os
from configparser import ConfigParser


def load_config(config_file_name: str) -> ConfigParser:
    base_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    config_file = os.path.join(base_folder, config_file_name)

    if not os.path.exists(config_file) or not os.path.isfile(config_file):
        raise Exception("No config file")

    config = ConfigParser()
    config.read(config_file, encoding='utf-8')

    return config