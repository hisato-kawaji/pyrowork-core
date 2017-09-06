#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import boto3
import sys
import os
import json
from framework import Config, Executor
from framework import Exceptions as ex


def attribute(name, value):
    return {"Name": name, "Value": value}


def confirm(event, context):
    def main(event, context):
        user_attributes = [].append(attribute('email_verified', 'true'))
        cognito_client = boto3.client('cognito-idp')
        cognito_client.admin_update_user_attributes(
            UserPoolId=Config().cognito_user_pool_id,
            Username=event['UserName'],
            UserAttributes=user_attributes
        )
        lambda_client = boto3.client('lambda')
        lambda_response = lambda_client.invoke(
            FunctionName=Config.create_function_name,
            Payload=json.dumps(event),
            Qualifier='Release'
        )

        return lambda_response

    return Executor.run(main, event, context)


def update(event, context):
    def main(event, context):
        user_attributes = []
        client = boto3.client('cognito-idp')
        return client.admin_update_user_attributes(
            UserPoolId=Config().coginito_user_pool_id,
            Username=event['user_name'],
            UserAttributes=user_attributes
        )
    return Executor.run(main, event, context)


def forget_password(event, context):
    def main(event, context):
        client = boto3.client('cognito-idp')
        return client.forgot_password(
            ClientId=Config().cognito_client_id,
            Username=event['path']['username']
        )
    return Executor.run(main, event, context)


if __name__ == '__main__':
    print('Cannot execute lambda functions directory. Try to use test console command')
