#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import boto3
import sys
import os
from framework import Config, Executor
from framework import Exceptions as ex


def get_by_id(event, context):
    def main(event, context):
        print(Config().TERM)
        raise Exception('hoge')

    Executor.run(main, event, context)

    return 'get_by_id'


def get_all(event, context):
    try:
        print("execute")
    except Exception as e:
        print("type:{0}".format(type(e)))
        print("args:{0}".format(e.args))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        print("Error Detail:", sys.exc_info()[1])
        raise
    return 'get-all'


def create(event, context):
    try:
        print("execute")
    except Exception as e:
        print("type:{0}".format(type(e)))
        print("args:{0}".format(e.args))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        print("Error Detail:", sys.exc_info()[1])
        raise
    return 'create'


def update(event, context):
    try:
        print("execute")
    except Exception as e:
        print("type:{0}".format(type(e)))
        print("args:{0}".format(e.args))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        print("Error Detail:", sys.exc_info()[1])
        raise
    return 'update'


def delete(event, context):
    try:
        print("execute")
    except Exception as e:
        print("type:{0}".format(type(e)))
        print("args:{0}".format(e.args))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        print("Error Detail:", sys.exc_info()[1])
        raise
    return 'delete'


if __name__ == '__main__':
    get_by_id(None, None)
    print('Cannot execute lambda functions directory. Try to use test console command')

