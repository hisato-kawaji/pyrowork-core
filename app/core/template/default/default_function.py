#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import boto3
import sys
import os
from framework import Config, Executor
from framework import Exceptions as ex


def lambda_handler(event, context):
    def main(event, context):

    return Executor.run(main, event, context)



if __name__ == '__main__':
    print('Cannot execute lambda functions directory. Try to use test console command')

