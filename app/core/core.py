#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import datetime
from datetime import datetime as dt
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

    def now(self):
        return (dt.utcnow() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')

class Executor:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Executor, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    @classmethod
    def run(cls, function, event, content):
        '''
            running lambda handler
        '''
        try:
            ret = function(event, content)
        except (ex.PyroException, Exception) as pe:
            if isinstance(pe, ex.PyroException):
                message = 'statusCode:' + str(pe.st_code) + ':' + pe.errmsg
                raise Exception(message)
            else:
                message = 'statusCode:500: Internal Server Error'
                raise Exception(message)
        else:
            return ret
