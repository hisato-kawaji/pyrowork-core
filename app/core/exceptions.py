#!/usr/bin/env python
# -*- coding: utf-8 -*-


class PyroException(BaseException):
    st_code = 500
    errmsg = 'Unknown invalid requests'


class NoRecordsException(PyroException):
    '''
        response when no data was hit by your search query
    '''

    st_code = 404
    errmsg = 'No records was found through your query'


class InvalidParamException(PyroException):
    '''
        response error on validation of your request parameters
    '''

    st_code = 403
    errmsg = 'Invalid parameters in your requests'


class InvalidAuthException(PyroException):
    '''
        response error on validation of your authentication
    '''

    st_code = 403
    errmsg = 'Invalid access to someone\'s data'


class ResourceException(PyroException):
    '''
        response error from AWS infrastructure across from lambda
    '''

    st_code = 503
    errmsg = 'Returned error from the service layer in AWS'


class FunctionException(PyroException):
    '''
        response error in lambda function( ex. typo, TypeError, etc...)
    '''

    st_code = 500
    errmsg = 'No records was found through your query'
