#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import decimal
import boto3
from framework import Config, Executor
from framework import Exceptions as ex


def get_by_id(event, context):
    def main(event, context):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(Config().table_name)
        response = table.get_item(
            Key={
                'user_id': event['path']['user_id'],
                'menu_id': decimal.Decimal(event['path']['menu_id'])
            }
        )

        if not response.get('Item'):
            raise ex.NoRecordsException(
                '%s:%s is not found' % (Config().table_name, event['path']['id'])
            )

        return response['Item']

    return Executor.run(main, event, context)


def save(event, context):
    def main(event, context):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(Config().table_name)

        duplicate_key = {
            'user_id': event['body']['user_id'],
            'menu_id': decimal.Decimal(event['body']['menu_id'])
        }
        latest_record = table.get_item(Key=duplicate_key)

        if 'Item' not in latest_record:
            latest_record.update(event['body'])
            latest_record['updated_at'] = Config().now()

        else:
            latest_record = {
                'user_id': None,
                'memu_id': None,
                'started_at': None,
                'created_at': Config().now(),
                'updated_at': Config().now()
            }
            latest_record.update(event['body'])
            # TODO:event['body']に入ってくる指定のカラムのみをDecimalに変換する仕組みを作る
            latest_record['menu_id'] = decimal.Decimal(latest_record['menu_id'])
        response = table.put_item(Item=latest_record)

        return response

    return Executor.run(main, event, context)


if __name__ == '__main__':
    print('Cannot execute lambda functions directory. Try to use test console command')
