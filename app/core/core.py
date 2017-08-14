#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import exceptions as ex


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
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Executor, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def run(self, function, event, content):
        '''
            runing lambda handler
        '''
        try:
            ret = function(event, content)
        except ex.PyroException as e:
            message = str(e.st_code) + ':' + e.errmsg + ' type:' + type(e)
            raise Exception(message)
        except Exception as e:
            raise e
        else:
            return ret
