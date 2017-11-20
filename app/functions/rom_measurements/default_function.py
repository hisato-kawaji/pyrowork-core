#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import decimal
import datetime
from datetime import timezone, timedelta
import boto3
from framework import Config, Executor
from framework import Exceptions as ex
from boto3.dynamodb.conditions import Key


def get_by_id(event, context):
    def main(event, context):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(Config().table_name)

        if event['path'].get('created_at', None):
            jst = timezone(timedelta(hours=+9), 'JST')
            created_at = datetime.datetime.fromtimestamp(int(event['path']['created_at']), jst)
            keys = {
                'user_id': event['path']['user_id'],
                'created_at': created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
            response = table.get_item(
                Key=keys
            )

        elif event['path'].get('item_id', None):
            user_cond = Key('user_id').eq(event['path']['user_id'])
            item_cond = Key('item_id').eq(event['path']['item_id'])
            response = table.query(
                IndexName='UserId-ItemId',
                KeyConditionExpression=user_cond & item_cond
            )

        else:
            user_cond = Key('user_id').eq(event['path']['user_id'])

            response = table.query(
                KeyConditionExpression=user_cond
            )

        if not response.get('Item') and not response.get('Items'):
            raise ex.NoRecordsException(
                '%s:%s is not found' % (Config().table_name, event['path']['user_id'])
            )

        if response.get('Items'):
            return response['Items']
        else:
            return response['Item']

    return Executor.run(main, event, context)


def create(event, context):
    def main(event, context):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(Config().table_name)

        rom_measurement = {
            'user_id': None,
            'item_id': None,
            'position': None,
            'angle': None,
            'init_angle': None,
            'started_at': None,
            'created_at': Config().now(),
            'updated_at': Config().now()
        }

        rom_measurement.update(event['body'])
        rom_measurement['item_id'] = decimal.Decimal(rom_measurement['item_id'])
        response = table.put_item(Item=rom_measurement)

        return response

    return Executor.run(main, event, context)


if __name__ == '__main__':
    print('Cannot execute lambda functions directory. Try to use test console command')
