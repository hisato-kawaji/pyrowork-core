#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import boto3
import sys
import os
from datetime import datetime
from framework import Config, Executor
from framework import Exceptions as ex
from boto3.dynamodb.conditions import Key


def get_record_by_unique(event, context):
    def main(event, context):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(Config().table_name)
        if event['path']['measure_type']:
            keys = {
                'user_id': event['path']['user_id'],
                'started_at': event['path']['started_at'],
                'measure_type': event['path']['measure_type']
            }
            response = table.get_item(
                Keys=keys
            )

        else:
            user_cond = Key('user_id').eq(event['path']['id'])
            start_cond = Key('started_at').eq(event['path']['start'])

            response = table.query(
                KeyConditionExpression=user_cond & start_cond
            )

        if not response.get('Item') and not response.get('Items'):
            raise ex.NoRecordsException(
                '%s:%s is not found' % (Config().table_name, event['path']['id'])
            )

        return response

    return Executor.run(main, event, context)


def get_stream_by_unique(event, context):
    def main(event, context):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(Config().table_name)
        walking_cond = Key('walking_id').eq(event['path']['walking_id'])
        if event['path']['measure_type']:
            type_cond = Key('started_at').eq(event['path']['measure_type'])
            response = table.query(
                KeyConditionExpression=walking_cond & type_cond
            )

        else:
            response = table.query(
                KeyConditionExpression=walking_cond
            )

        if not response.get('Items'):
            raise ex.NoRecordsException(
                '%s:%s is not found' % (Config().table_name, event['path']['id'])
            )

        return response

    return Executor.run(main, event, context)


def create(event, context):
    def main(event, context):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(Config().table_name)

        user_id = event['event']['user_id']
        duplicate_key = {
            'id': user_id,
            'started_at': event['body']['started_at'],
            'measure_type': event['body']['measure_type']
        }

        if table.get_item(Keys=duplicate_key):
            raise ex.InvalidValueExvception('Duplicated primary key')

        user = {
            'user_id': user_id,
            'started_at': None,
            'ended_at': None,
            'created_at': datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        }

        user.update(event['body'])
        response = table.put_item(Item=user)

        return response

    return Executor.run(main, event, context)


if __name__ == '__main__':
    print('Cannot execute lambda functions directory. Try to use test console command')