#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
import argparse


def make_function():

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--function', type=str, required=True,
                        help='Lambda Function name')
    parser.add_argument('-s', '--scafolding', action="store_true",
                        help='valid scafolding')
    args = parser.parse_args()
    function_name = args.function
    is_scafold = args.scafolding

    try:
        if os.path.exists('../functions/' + function_name):
            raise Exception('function name is duplicated, should be changed.')

        if is_scafold:
            shutil.copytree('./template/scafold/', '../functions/' + function_name + '/')
        else:
            shutil.copytree('./template/default/', '../functions/' + function_name + '/')

    except Exception as e:
        print(e.args)
        print(e)
        exit()


if __name__ == '__main__':
    make_function()
