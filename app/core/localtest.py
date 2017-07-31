#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import argparse
import importlib
sys.path.append('../functions/')


def test_console():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--event', type=str, required=False,
                        help='Event variables for Test')
    parser.add_argument('-c', '--context', type=str, required=False,
                        help='Context variables for Test')
    parser.add_argument('-f', '--function', type=str, required=True,
                        help='Lambda Function name')
    parser.add_argument('-l', '--handler', type=str, required=True,
                        help='Lambda Event Handler name')
    args = parser.parse_args()
    event = args.event
    context = args.context
    lambda_function = args.function
    event_handler = args.handler

    test_module = importlib.import_module(
        lambda_function + '.default_function'
    )
    method = getattr(test_module, event_handler)
    assert method(event, context), 'assertion: ' + lambda_function + ':' + event_handler


if __name__ == '__main__':
    test_console()
