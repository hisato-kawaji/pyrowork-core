#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import boto3
import sys
import os
import json
import base64
from framework import Config, Executor
from framework import Exceptions as ex


def create_stream(event, context):
    def main(event, context):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(Config().table_name)
        with table.batch_writer() as batch:
            for record in event['Records']:
                new_data = json.loads(base64.b64decode(record['kinesis']['data']).decode('utf-8'))
                batch.put_item(
                    Item=new_data
                )

        return 'Successfully processed {} records.'.format(len(event['Records']))

    return Executor.run(main, event, context)


if __name__ == '__main__':
    print('Cannot execute lambda functions directory. Try to use test console command')
