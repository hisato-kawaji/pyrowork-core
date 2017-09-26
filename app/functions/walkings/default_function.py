#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import boto3
from framework import Config, Executor
from framework import Exceptions as ex
from boto3.dynamodb.conditions import Key


def get_record_by_unique(event, context):
    def main(event, context):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(Config().table_name)
        user_cond = Key('user_id').eq(event['path']['user_id'])
        start_cond = Key('started_at').eq(event['path']['started_at'])
        response = table.query(
            KeyConditionExpression=user_cond & start_cond
        )
        if not response.get('Items'):
            raise ex.NoRecordsException(
                '%s:%s:%s is not found' % (
                    Config().table_name,
                    event['path']['user_id'],
                    event['path']['started_at']
                )
            )

        if event['path'].get('measure_type', None):
            for item in response['Items']:
                if item['measure_type'] == event['path']['measure_type']:
                    return item

            raise ex.NoRecordsException(
                '%s:%s:%s:%s is not found' % (
                    Config().table_name,
                    event['path']['user_id'],
                    event['path']['started_at'],
                    event['path']['measure_type']
                )
            )
        else:
            return response['Items']

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

        return response['Responses'][Config().table_name]

    return Executor.run(main, event, context)


def create(event, context):
    def main(event, context):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(Config().table_name)

        duplicate_key = {
            'user_id': event['body']['user_id'],
            'started_at': event['body']['started_at'],
        }

        duplicated = table.get_item(Key=duplicate_key)
        if 'Item' in duplicated:
            raise ex.InvalidValueException('Duplicated primary key')

        user = {
            'user_id': None,
            'started_at': None,
            'ended_at': None,
            'created_at': Config().now(),
            'updated_at': Config().now()
        }

        user.update(event['body'])
        response = table.put_item(Item=user)

        return response

    return Executor.run(main, event, context)


if __name__ == '__main__':
    print('Cannot execute lambda functions directory. Try to use test console command')
