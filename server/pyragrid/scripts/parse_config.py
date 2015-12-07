#!/usr/bin/env python
import argparse
import subprocess
from pprint import pprint
import os.path
from os.path import dirname, realpath, join as path_join
import configparser
from urllib.parse import urlparse, urlsplit

current_dir_path = dirname(realpath(__file__))
server_dir_path = dirname(dirname(current_dir_path))

quote = lambda string: '"' + string + '"'


# see https://gist.github.com/mmerickel/7901444
def ini_file_to_dict(file_name):
    config = configparser.ConfigParser()
    config.read(file_name)
    # db_url = config.get('app:main', 'sqlalchemy.url')
    d = dict(config._sections)
    for k in d:
        d[k] = dict(config._defaults, **d[k])
        d[k].pop('__name__', None)
    return d


# see http://stackoverflow.com/a/7205234/1760643
def dicts_merge(dictionary1, dictionary2):
    output = {}
    for key1, value1 in dictionary1.items():
        if key1 in dictionary2:
            if isinstance(dictionary2[key1], dict):
                output[key1] = dicts_merge(value1, dictionary2.pop(key1))
        else:
            output[key1] = value1
    for key2, value2 in dictionary2.items():
        output[key2] = value2
    return output


def get_ini_path(ini_name):
        #TODO consistency with get_ini_path
    if not ini_name.endswith('.ini'):
        ini_name += '.ini'
    return realpath(path_join(server_dir_path, ini_name))


def get_passwords_ini_path(ini_name):
    file_name, file_ext = os.path.splitext(ini_name)
    if file_ext == '':
        file_ext = '.ini'
    passwords_ini_path = realpath(path_join(server_dir_path, file_name + '_passwords' + file_ext))
    if os.path.isfile(passwords_ini_path):
        return passwords_ini_path
    return None


def load_merged_ini(ini_name):
    ini_path = get_ini_path(ini_name)
    if not os.path.isfile(ini_path):
        raise Exception('File ' + quote(ini_path) + ' not found')
    settings = ini_file_to_dict(ini_path)
    # TODO process [overriden by] section in ini with file lists
    passwords_ini_path = get_passwords_ini_path(ini_name)
    if passwords_ini_path:
        passwords_settings = ini_file_to_dict(passwords_ini_path)
        settings = dicts_merge(settings, passwords_settings)
    return settings


def ini_get(ini: dict, section: str, option: str):
    ini_section = ini.get(section)
    if ini_section is None:
        return None
    return ini_section.get(option)


def get_connection_url_from_settings(ini: dict) -> str:
    db_url = ini_get(ini, 'app:main', 'sqlalchemy.url')
    if db_url is None:
        return None

    return db_url


def db_connection_params_from_url(db_url: str) -> dict:
    if db_url is None:
        return None

    splitted_url = urlsplit(db_url)

    conn_params = dict(url=db_url)

    conn_params['dbms'] = splitted_url.scheme
    conn_params['name'] = splitted_url.path.strip('/')
    loc = splitted_url.netloc
    at_sign_split = loc.split('@')
    if len(at_sign_split) != 2:
        return conn_params
    conn_params['host'] = at_sign_split[1]
    semicolon_split = at_sign_split[0].split(':')
    if len(semicolon_split) != 2:
        return conn_params
    conn_params['username'] = semicolon_split[0]
    conn_params['password'] = semicolon_split[1]
    return conn_params


def main():
    arg_parser = argparse.ArgumentParser(description='read info from config')
    arg_parser.add_argument(
            '--config', '-c',
            help='config name',
            default='development'
    )
    arg_parser.add_argument(
            'action',
            choices=['db'],
    )
    # TODO help for action_params:
    arg_parser.add_argument('action_params', nargs='*', help='for db action: user/password/url/name')
    args = arg_parser.parse_args()
    ini_path = get_ini_path(args.config)
    ini = load_merged_ini(args.config)
    # pprint(args)
    if args.action == 'db':
        pass
        db_url = get_connection_url_from_settings(ini)
        if db_url is None:
            raise Exception('Can\'t parse db url from ' + quote(ini_path))
        connection_params = db_connection_params_from_url(db_url)
        if not args.action_params or len(args.action_params) == 0:
            for (param, value) in connection_params.items():
                print(param + '=' + value)
        else:
            key = args.action_params[0]
            value = connection_params.get(key)
            if value:
                print(value)
            else:
                raise Exception(
                    'Wrong db connection params key name. Available keys are: ' + ', '.join(connection_params.keys()))
    else:
        print('Unknown action ' + args.action)


if __name__ == "__main__":
    main()
