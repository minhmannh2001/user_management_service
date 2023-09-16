import os

import flask_jwt_extended
import yaml
from passlib.hash import pbkdf2_sha256


def load_yaml_file(config_file):
    with open(config_file, 'r') as f:
        return yaml.safe_load(f.read())


def load_config_from_yaml_file(config_file):
    if not os.path.isabs(config_file):
        raise Exception('The configuration file MUST be specified using an absolute path.')
    config = load_yaml_file(config_file)
    return config


def update_config_from_environment(config):
    for key in config:
        config[key] = os.environ.get(key, config[key])
    return config


def load_config(from_file=None, env=True):
    config = {}
    if from_file is not None:
        config = load_config_from_yaml_file(from_file)
    if env:
        return update_config_from_environment(config)
    return config


def decode_token(token):
    if token and token.startswith('Bearer '):
        return flask_jwt_extended.decode_token(token[7:])
    else:
        return flask_jwt_extended.decode_token(token)


def hash_password(password):
    hashed_password = pbkdf2_sha256.using(rounds=1000, salt_size=16).hash(password)
    return hashed_password


def verify_password(user_password, hashed_password):
    return pbkdf2_sha256.verify(user_password, hashed_password)

