#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import boto3
import sys
import os
import uuid
from datetime import datetime
from framework import Config, Executor
from framework import Exceptions as ex
from boto3.dynamodb.conditions import Key


def get_by_id(event, context):
    def main(event, context):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(Config().table_name)
        response = table.get_item(
            Key={'id': event['path']['id']}
        )

        if not response.get('Item'):
            raise ex.NoRecordsException(
                '%s:%s is not found' % (Config().table_name, event['path']['id'])
            )

        return response['Item']

    return Executor.run(main, event, context)


def get_by_institution_id(event, context):
    def main(event, context):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(Config().table_name)
        key_condition = Key('institution_id').eq(event['path']['id'])
        response_users = table.query(
            IndexName='UserId-InstitutionId',
            KeyConditionExpression=key_condition
        )

        user_list = []
        for item in response_users['Items']:
            user_list.append({'id': item['id']})

        if user_list == []:
            raise ex.NoRecordsException(
                '%s:institution_id=%s is not found' % (Config().table_name, event['path']['id'])
            )

        response = dynamodb.batch_get_item(RequestItems={
            Config().table_name: {
                'Keys': user_list
            }
        })

        return response['Responses'][Config().table_name]

    return Executor.run(main, event, context)


def create(event, context):
    def main(event, context):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(Config().table_name)

        user_id = str(uuid.uuid4())
        duplicate_key = {
            'id': user_id,
            'institution_id': event['body']['institution_id']
        }
        duplicated = table.get_item(Key=duplicate_key)
        if 'Item' in duplicated:
            raise ex.InvalidValueException('Duplicated primary key')

        user = {
            'id': user_id,
            'institution_id': None,
            'patient_id': None,
            'family_name': None,
            'last_name': None,
            'family_name_kana': None,
            'last_name_kana': None,
            'nc_level': None,
            'gender': None,
            'birthday': None,
            'entered_at': None,
            'left_at': None,
            'created_at': datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        }

        user.update(event['body'])
        response = table.put_item(Item=user)

        return response

    return Executor.run(main, event, context)


def update(event, context):
    def main(event, context):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(Config().table_name)

        duplicate_key = {
            'id': event['path']['user_id']
        }

        user_old = table.get_item(Key=duplicate_key)
        if 'Item' not in user_old:
            raise ex.NoRecordsException(
                '%s:%s is not fount' % (Config().table_name, event['path']['user_id'])
            )
        user = user_old['Item']
        user.update(event['body'])
        user['updated_at'] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        response = table.put_item(Item=user)

        return response

    return Executor.run(main, event, context)


if __name__ == '__main__':
    print('Cannot execute lambda functions directory. Try to use test console command')
