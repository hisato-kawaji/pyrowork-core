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
        summary_cond = Key('user_id').eq(event['path']['id']) & \
            Key('measure_type').eq(event['path']['type'])
        response = table.query(
            IndexName='WalkingSummary',
            KeyConditionExpression=summary_cond
        )

        if not response.get('Items'):
            raise ex.NoRecordsException(
                '%s:%s is not found' % (Config().table_name, event['path']['id'])
            )

        return response

    return Executor.run(main, event, context)


def get_by_time(event, context):
    def main(event, context):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(Config().table_name)
        response = table.get_item(
            Key={
                'user_id': event['path']['id'],
                'started_at': event['path']['started_at']
            }
        )

        return response

    return Executor.run(main, event, context)


def create(event, context):
    def main(event, context):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(Config().table_name)

        user_id = event['body']['user_id']
        duplicate_key = {
            'id': user_id,
            'started_at': event['body']['started_at'],
            'measure_type': event['body']['measure_type']
        }

        duplicated = table.get_item(Keys=duplicate_key)
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
