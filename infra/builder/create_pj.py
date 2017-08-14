#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import boto3
import yaml
import argparse
from boto3 import Session

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--profile', type=str, required=True,
                    help='input aws profile name (DO NOT USE DEFAULT PROFILE)')

def main():
    args = parser.parse_args()
    profile = args.profile

    try:
        session = Session(profile_name=profile)
        client = session.client('codebuild')
        with open('{your lambda cloudformation template yaml file}') as f:
            lambda_setting = yaml.safe_load(f)
        for key, value in lambda_setting['Resources'].items():
            table_name = str(value['Properties']['Description'])
            response = client.create_project(
                name=key,
                description='string',
                source={
                    'type': 'GITHUB',
                    'location': 'https://github.com/{path}.git',
                    'auth': {
                        'type': 'OAUTH',
                    }
                },
                artifacts={
                    'type': 'S3',
                    'location': '{s3 bucket name}',
                    'namespaceType': 'NONE',
                    'name': key,
                    'packaging': 'ZIP'
                },
                environment={
                    'type': 'LINUX_CONTAINER',
                    'image': 'aws/codebuild/python:3.5.2',
                    'computeType': 'BUILD_GENERAL1_SMALL',
                    'environmentVariables': [
                        {
                            'name': 'TARGET_DIRECTORY',
                            'value': table_name
                        },
                    ],
                    'privilegedMode': False
                },
                serviceRole='{your code build role arn}',
                timeoutInMinutes=60,
                encryptionKey='{your kms arn for s3}'
            )
            print('created build porject:', key)

    except:
        print('Unexpected error:', sys.exc_info()[0])
        print('Erro Detail:', sys.exc_info()[1])
        exit()


if __name__ == '__main__':
    main()

