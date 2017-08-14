#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
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
        client = session.client('lambda')
        with open('{your lambda cloudformation template yaml file}') as f:
            lambda_setting = yaml.safe_load(f)
        for key, value in lambda_setting['Resources'].items():
            if value['Type'] == 'AWS::Serverless::Function':
                version_list = []
                response = client.list_versions_by_function(
                    FunctionName=value['Properties']['FunctionName'],
                    MaxItems=20
                )

                for function in response['Versions']:
                    print(function['Version'])
                    version_list.append(function['Version'])

                while 'NextMarker' in response:
                    response = client.list_versions_by_function(
                        FunctionName=value['Properties']['FunctionName'],
                        MaxItems=20,
                        Marker=response['NextMarker']
                    )
                    for function in response['Versions']:
                        version_list.append(function['Version'])
                print(value['Properties']['FunctionName'] + ' max version: ' + str(max(version_list)))
                attach = client.create_alias(
                    FunctionName=value['Properties']['FunctionName'],
                    Name='Release',
                    FunctionVersion=str(max(version_list)),
                    Description='release version'
                )
                print(attach)

    except:
        print('Unexpected error:', sys.exc_info()[0])
        print('Error Detail:', sys.exc_info()[1])
        exit()


if __name__ == '__main__':
    main()
