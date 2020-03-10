#!/usr/bin/env python3
from argparse import ArgumentParser

import email.utils
import itertools
import os
import sys

DEFAULT_SEPARATORS = '~`!@#$%^&*()_+-={}|[]\\:";\'<>?,./ \t'
DEFAULT_TIMESTAMP_OFFSET = 1
EXAMPLE_DATE = 'Tue, 10 Mar 2020 14:06:36 GMT'
TIMESTAMP_PLACEHOLDER = '__TIMESTAMP_HERE__'
VERSION = '1.1'


def print_error(message):
    sys.stderr.write('[!] %s%s' % (message, os.linesep))


def die(message):
    print_error(message)
    sys.exit(1)


def parse_date(value):
    try:
        return int(email.utils.parsedate_to_datetime(value).timestamp())
    except (TypeError, ValueError):
        die('Invalid date format (example: %s)' % EXAMPLE_DATE)


def parse_timestamp_offset(value):
    try:
        timestamp_offset = int(value)
        if timestamp_offset < 0:
            die('Invalid timestamp offset (must be 0 or greater)')
        return timestamp_offset
    except ValueError:
        die('Invalid timestamp offset format (must be integer)')


def prepare_data(args):
    return args.data


def prepare_timestamps(args):
    timestamps = []
    if args.date:
        timestamp = parse_date(args.date)
        timestamp_offset = parse_timestamp_offset(args.timestamp_offset)
        while timestamp_offset >= 0:
            timestamps.append(str(timestamp - timestamp_offset))
            timestamp_offset -= 1
    return timestamps


def prepare_separators(args):
    separators = list(set(args.separators))  # unique separators
    separators.append('')  # empty separator
    return separators


def parse_args():
    parser = ArgumentParser(description='Word list generator to crack security tokens v%s' % VERSION)
    parser.add_argument(
        '-d', '--date',
        help='timestamp from this date will be used as an additional data chunk, example: %s' % EXAMPLE_DATE
    )
    parser.add_argument(
        '-o', '--timestamp-offset',
        help='how many previous (to timestamp from date) timestamps should be used as an additional data chunk, default: %d' % DEFAULT_TIMESTAMP_OFFSET,
        default=DEFAULT_TIMESTAMP_OFFSET
    )
    parser.add_argument(
        '-s', '--separators',
        help='data chunks separators to check, default: %s' % DEFAULT_SEPARATORS.replace('%', '%%').replace('\t', '\\t'),
        default=DEFAULT_SEPARATORS
    )
    parser.add_argument(
        'data',
        help='data chunks',
        nargs='+'
    )
    args = parser.parse_args(sys.argv[1:])
    return prepare_data(args), prepare_timestamps(args), prepare_separators(args)


def print_permutation(permutation, timestamps):
    if TIMESTAMP_PLACEHOLDER in permutation:
        for timestamp in timestamps:
            print(permutation.replace(TIMESTAMP_PLACEHOLDER, timestamp))
    else:
        print(permutation)


def print_permutations(data, timestamps, separators):
    if len(timestamps) > 0:
        data.append(TIMESTAMP_PLACEHOLDER)
    for r in range(1, len(data) + 1):
        for permutation in itertools.permutations(data, r):
            if len(permutation) > 1:
                for separator in separators:
                    print_permutation(separator.join(permutation), timestamps)
            else:
                print_permutation(permutation[0], timestamps)


def main():
    data, timestamps, separators = parse_args()
    print_permutations(data, timestamps, separators)


if __name__ == '__main__':
    main()
