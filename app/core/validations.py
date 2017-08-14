#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Validator:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(PyroValidator, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def valid_int(): pass
    def valid_decimal(): pass
    def valid_float(): pass
    def valid_string(): pass
    def valid_datetime(): pass
    def valid_date(): pass
    def valid_format(regex): pass

