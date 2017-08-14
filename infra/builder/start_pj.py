#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import boto3
import yaml
import argparse
import time
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
        i = 0;
        build_status = []
        for key, value in lambda_setting['Resources'].items():
            response = client.start_build(
                projectName=key
            )
            build_status.append(response['build']['id'])
            print('building project:', response['build']['id'])

            if  (i % 15 == 0 and i != 0) or i + 1 == len(lambda_setting['Resources']):
                incompleted_flag = True
                while incompleted_flag:
                    get_status = client.batch_get_builds(ids=build_status)
                    check_builds = get_status['builds']
                    wait_flag = False
                    wait_count = 0
                    for build in check_builds:
                        if build['buildComplete'] == False:
                            wait_flag = True
                            print(build['id'], ' is waiting for build-complete...')
                        else:
                            wait_count = wait_count + 1

                    if wait_flag:
                        print (str(wait_count) + ' / ' + str(len(build_status))  + 'were build-completed')
                        time.sleep(3)
                        continue
                    incompleted_flag = False
                    for build_id in build_status:
                        print('build-completed: ', build_id)
                    build_status = []
            i = i + 1

    except:
        print('Unexpected error:', sys.exc_info()[0])
        print('Erro Detail:', sys.exc_info()[1])
        exit()

if __name__ == '__main__':
    main()

