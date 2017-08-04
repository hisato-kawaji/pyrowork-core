#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os

class Config:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Config, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self, *args, **kwargs):
        for key, value in os.environ.items():
            setattr(self, key, value)


class Executor:

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Executor, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self, *args, **kwargs):
        for key, value in os.environ.items():
            setattr(self, key, value)

    def run(function, *args):
        try:
            ret = function(*args)
            return ret
        except Exception as e:
            print("type:{0}".format(type(e)))
            print("args:{0}".format(e.args))
        except:
              print("Unexpected error:", sys.exc_info()[0])
