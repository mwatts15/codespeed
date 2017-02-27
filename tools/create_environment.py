#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""
Check if an environment exists, create otherwise
"""
from __future__ import print_function
import json
from six.moves.urllib.request import Request, build_opener, urlopen
from six.moves.urllib.error import HTTPError
from optparse import OptionParser
import simplejson

CODESPEED_URL = 'http://localhost:8000'


def get_options():
    """Get the options and arguments
    """
    parser = OptionParser()

    parser.add_option("-e", "--environment", dest="environment",
                      help="name of the environment to create")

    (options, args) = parser.parse_args()

    if not options.environment:
        parser.error("No environment given")

    return options, args


def is_environment(environment):
    """check if environment does exist

        return:
            True if it exist
            False if it doesn't exist
    """
    url = CODESPEED_URL + '/api/v1/environment/'
    request = Request(url)
    opener = build_opener()
    try:
        raw_data = opener.open(request)
    except HTTPError as e:
        raise e
    data = simplejson.load(raw_data)
    if environment in [env['name'] for env in data['objects']]:
        return True
    return False


def create_environment(environment):
    """create the environment

        return:
            True if success
            False if not created
    """
    url = CODESPEED_URL + '/api/v1/environment/'
    data = json.dumps({'name': environment})
    request = Request(url, data, {'Content-Type': 'application/json'})
    try:
        f = urlopen(request)
        response = f.read()
        f.close()
    except HTTPError as e:
        raise e
    return response


def main():
    (options, args) = get_options()
    if is_environment(options.environment):
        print("Found environment, doing nothing.")
    else:
        print(create_environment(options.environment))


if __name__ == "__main__":
    main()
