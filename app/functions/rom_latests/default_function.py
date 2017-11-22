#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import decimal
import boto3
from framework import Config, Executor
from framework import Exceptions as ex
from boto3.dynamodb.conditions import Key


def get_by_id(event, context):
    def main(event, context):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(Config().table_name)
        response = table.get_item(
            Key={
                'user_id': event['path']['user_id'],
                'item_position_id': event['path']['item_id']
            }
        )

        if not response.get('Item'):
            raise ex.NoRecordsException(
                '%s:%s is not found' % (Config().table_name, event['path']['user_id'])
            )

        return response['Item']

    return Executor.run(main, event, context)


def get_by_user_id(event, context):
    def main(event, context):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(Config().table_name)
        response = table.query(
            KeyConditionExpression=Key('user_id').eq(event['path']['id'])
        )

        if not response.get('Items'):
            raise ex.NoRecordsException(
                '%s:%s is not found' % (Config().table_name, event['path']['user_id'])
            )

        return response['Items']

    return Executor.run(main, event, context)


def save(event, context):
    def main(event, context):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(Config().table_name)

        duplicate_key = {
            'user_id': event['body']['user_id'],
            'item_position_id': event['body']['item_position_id']
        }
        latest_record = table.get_item(Key=duplicate_key)

        if 'Item' not in latest_record:
            latest_record.update(event['body'])
            latest_record['updated_at'] = Config().now()

        else:
            latest_record = {
                'user_id': None,
                'item_position_id': None,
                'started_at': None,
                'created_at': Config().now(),
                'updated_at': Config().now()
            }
            latest_record.update(event['body'])
        response = table.put_item(Item=latest_record)

        return response

    return Executor.run(main, event, context)


if __name__ == '__main__':
    print('Cannot execute lambda functions directory. Try to use test console command')
