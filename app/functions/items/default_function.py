#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import boto3
import decimal
from framework import Config, Executor
from framework import Exceptions as ex
from boto3.dynamodb.conditions import Key


def get_by_id(event, context):
    def main(event, context):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(Config().table_name)
        response = table.get_item(
            Key={
                'part': event['path']['part'],
                'id': decimal.Decimal(event['path']['id'])
            }
        )

        if not response.get('Item'):
            raise ex.NoRecordsException(
                '%s:%s is not found' % (Config().table_name, event['path']['id'])
            )

        return response['Item']

    return Executor.run(main, event, context)


def get_by_part(event, context):
    def main(event, context):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(Config().table_name)
        response = table.query(
            KeyConditionExpression=Key('part').eq(event['path']['part'])
        )

        if not response.get('Items'):
            raise ex.NoRecordsException(
                '%s:%s is not found' % (Config().table_name, event['path']['part'])
            )

        return response['Items']

    return Executor.run(main, event, context)


if __name__ == '__main__':
    print('Cannot execute lambda functions directory. Try to use test console command')
