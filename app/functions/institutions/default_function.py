#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import boto3
import uuid
from framework import Config, Executor
from framework import Exceptions as ex


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


def get_all(event, context):
    def main(event, context):

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(Config().table_name)
        response = table.scan()

        if not response.get('Items'):
            raise ex.NoRecordsException(
                '%s is not found' % Config().table_name
            )

        data = response['Items']

        while 'LastEvaluatedKey' in response:
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
        if 'id' in event['body']:
            raise ex.InvalidValueException('You cannot include id column in your request object')

        institution_id = str(uuid.uuid4())
        duplicate_key = {
            'id': institution_id
        }

        duplicated = table.get_item(Key=duplicate_key)
        if 'Item' in duplicated:
            raise ex.InvalidValueException('Duplicated primary key')

        institution = {
            'id': institution_id,
            'cognito_sub': None,
            'name': None,
            'admin': None,
            'username': None,
            'email': None,
            'company': None,
            'company_kana': None,
            'registerd_at': None,
            'created_at': Config().now(),
            'updated_at': Config().now()
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

        institution_old = table.get_item(Key=duplicate_key)
        if 'Item' not in institution_old:
            raise ex.NoRecordsException(
                '%s:%s is not fount' % (Config().table_name, institution_id)
            )
        institution = institution_old['Item']
        institution.update(event['body'])
        institution['updated_at'] = Config().now()
        response = table.put_item(Item=institution)

        # lambda_client = boto3.client('lambda')
        # lambda_response = lambda_client.invoke(
        #     FunctionName=Config().cognito_update_function_name,
        #     Payload=json.dumps(event),
        #     Qualifier='Release'
        # )

        # return lambda_response
        return response

    return Executor.run(main, event, context)


def delete(event, context):
    def main(event, context):
        pass

    return Executor.run(main, event, context)


if __name__ == '__main__':
    print('Cannot execute lambda functions directory. Try to use test console command')
