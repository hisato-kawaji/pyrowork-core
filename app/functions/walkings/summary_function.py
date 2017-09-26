#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import boto3
from framework import Config, Executor
from framework import Exceptions as ex
from boto3.dynamodb.conditions import Key


def get_by_type(event, context):
    def main(event, context):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(Config().table_name)
        summary_cond = Key('user_id').eq(event['path']['user_id']) & \
            Key('measure_type').eq(event['path']['type'])
        response = table.query(
            IndexName='WalkingSummary',
            KeyConditionExpression=summary_cond
        )

        if not response.get('Items'):
            raise ex.NoRecordsException(
                '%s:%s is not found' % (Config().table_name, event['path']['user_id'])
            )

        return response

    return Executor.run(main, event, context)


def get_by_time(event, context):
    def main(event, context):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(Config().table_name)
        response = table.get_item(
            Key={
                'user_id': event['path']['user_id'],
                'started_at': event['path']['started_at']
            }
        )

        if not response.get('Item'):
            raise ex.NoRecordsException(
                '%s:%s:%s is not found' % (
                    Config().table_name,
                    event['path']['id'],
                    event['path']['started_at']
                )
            )

        return response['Item']

    return Executor.run(main, event, context)


def create(event, context):
    def main(event, context):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(Config().table_name)

        duplicate_key = {
            'user_id':  event['body']['user_id'],
            'started_at': event['body']['started_at']
        }

        duplicated = table.get_item(Key=duplicate_key)
        if 'Item' in duplicated:
            raise ex.InvalidValueExvception('Duplicated primary key')

        user = {
            'user_id': None,
            'time': None,
            'measure_type': None,
            "r_lat_max": None,
            "r_lat_min": None,
            "l_lat_max": None,
            "l_lat_min": None,
            "r_foot_max": None,
            "r_foot_min": None,
            "l_foot_max": None,
            "l_foot_min": None,
            "front_behind": None,
            "left_right": None,
            'started_at': None,
            'created_at': Config().now(),
            'updated_at': Config().now()
        }

        user.update(event['body'])
        response = table.put_item(Item=user)

        return response

    return Executor.run(main, event, context)


if __name__ == '__main__':
    print('Cannot execute lambda functions directory. Try to use test console command')
