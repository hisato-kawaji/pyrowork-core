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
        with open('{your lambda cloudfromation template yaml file}') as f:
            lambda_setting = yaml.safe_load(f)
        for key, value in lambda_setting['Resources'].items():
            response = client.delete_project(
                name=key
            )
            print('deleted project:', key)

    except:
        print('Unexpected error:', sys.exc_info()[0])
        print('Erro Detail:', sys.exc_info()[1])
        exit()


if __name__ == '__main__':
    main()

