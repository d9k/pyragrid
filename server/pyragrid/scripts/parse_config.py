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


def ini_get(ini: configparser.RawConfigParser, section: str, option: str):
    if not ini.has_option(section, option):
        return None
    return ini.get(section, option)


def get_ini_path(ini_name):
    return realpath(path_join(server_dir_path, ini_name + '.ini'))


def get_connection_url_from_ini(ini_path: str) -> str:
    ini = configparser.RawConfigParser()
    ini.read(ini_path)

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
    # print(server_dir_path)
    ini_path = get_ini_path('development')
    # print(ini_path)

    if not os.path.isfile(ini_path):
        raise Exception('File ' + quote(ini_path) + ' not found')

    # TODO help for action_params:
    arg_parser.add_argument('action_params', nargs='*', help='for db action: user/password/url/name')
    args = arg_parser.parse_args()
    # pprint(args)
    if args.action == 'db':
        pass
        db_url = get_connection_url_from_ini(ini_path)
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
