#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import boto3
import sys
import os


class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        for key, value in os.environ.items():
            setattr(self, key, value)

    def get(key):
        return getattr(self, key)


class Executor:

    def run(function, *args):
        try:
            ret = function(*args)
            return ret
        except Exception as e:
            print("type:{0}".format(type(e)))
            print("args:{0}".format(e.args))
            print('Error poi')
        except:
            print("Unexpected error:", sys.exc_info()[0])



executor = Executor


def get_by_id(event, context):
    def main(event, context):
        raise Exception("error!")
        print('hogefuga-')

    executor.run(main, event, context)

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

