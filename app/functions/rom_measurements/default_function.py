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


def get_by_id(event, context):
    def main(event, context):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(Config().table_name)

        if event['path']['created'] and event['path']['item_id']:
            keys = {
                'user_id': event['path']['user_id'],
                'created_at': event['path']['created_at'],
                'item_id': event['path']['item_id']
            }
            response = table.get_item(
                Keys=keys
            )

        elif event['path']['created']:
            user_cond = Key('user_id').eq(event['path']['user_id'])
            start_cond = Key('created_at').eq(event['path']['created'])

            response = table.query(
                KeyConditionExpression=user_cond & start_cond
            )

        else:
            user_cond = Key('user_id').eq(event['path']['user_id'])

            response = table.query(
                KeyConditionExpression=user_cond & start_cond
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

        duplicate_key = {
            'user_id': event['path']['user_id'],
            'cognito_id': event['path']['created_at'],
            'item_id': event['path']['item_id']
        }

        if table.get_item(Keys=duplicate_key):
            raise ex.InvalidValueExvception('Duplicated primary key')

        rom_measurement = {
            'user': event['path']['user_id'],
            'item_id': None,
            'init_angle': None,
            'angle': None,
            'created_at': datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        }

        rom_measurement.update(event['body'])
        response = table.put_item(Item=rom_measurement)

        return response

    return Executor.run(main, event, context)


if __name__ == '__main__':
    print('Cannot execute lambda functions directory. Try to use test console command')
