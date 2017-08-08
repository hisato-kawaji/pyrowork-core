#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import boto3
import sys
import os
from datetime import datetime
from framework import Config, Executor
from framework import Exceptions as ex


def get_by_id(event, context):
    def main(event, context):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(Config().table_name)
        response = table.get_item(
            Keys={'id': event['path']['id']}
        )

        if not response.get('Item'):
            raise ex.NoRecordsException(
                '%s:%s is not found' % (Config().table_name, event['path']['id'])
            )

        return response

    return Executor.run(main, event, context)


def get_all(event, context):
    def main(event, context):

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(Config().table_name)
        response = table.scan()

        if not response.get('Item'):
            raise ex.NoRecordsException(
                '%s:%s is not found' % (Config().table_name, event['path']['id'])
            )

        data = response['Items']

        if 'LastEvaluatedKey' in response:
            response = table.scan(
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            data.extend(response['Items'])

        response['Items'] = data

        return response

    return Executor.run(main, event, context)


def create(event, context):
    def main(event, context):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(Config().table_name)

        institution_id = event['path']['id']
        duplicate_key = {
            'id': institution_id
        }

        if table.get_item(Keys=duplicate_key):
            raise ex.InvalidValueExvception('Duplicated primary key')

        institution = {
            'id': institution_id,
            'cognito_id': None,
            'name': None,
            'admin': None,
            'login_name': None,
            'email': None,
            'tel': None,
            'company': None,
            'company_kana': None,
            'registerd_at': None,
            'zipcode': None,
            'address': None,
            'fax': None,
            'created_at': datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        }

        institution.update(event['body'])
        response = table.put_item(Item=institution)

        return response

    return Executor.run(main, event, context)


def update(event, context):
    def main(event, context):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(Config().table_name)

        institution_id = event['path']['id']
        duplicate_key = {
            'id': institution_id
        }

        institution_old = table.get_item(Keys=duplicate_key)
        if not table.get_item(Keys=duplicate_key):
            raise ex.NoRecordExvception(
                '%s:%s is not fount' % (Config().table_name, institution_id)
            )
        institution = institution_old['Item']
        institution.update(event['body'])
        institution['updated_at'] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        response = table.put_item(Item=institution)

        return response

    return Executor.run(main, event, context)


def delete(event, context):
    def main(event, context):
        pass

    return Executor.run(main, event, context)


if __name__ == '__main__':
    print('Cannot execute lambda functions directory. Try to use test console command')
