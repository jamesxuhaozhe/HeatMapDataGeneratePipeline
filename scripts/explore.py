#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from geopy import distance as dis

def check_arg():
    if len(sys.argv) != 2:
        print('Invalid command line input! Your input should be something like \
        python explore.py path_to_file')

def read_file_and_calculate(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            data = line.split('\t')

            long_str = data[1].strip()
            lat_str = data[2].strip()
            
            before_location = (float(lat_str), float(long_str))
            converted_location = get_location_after_convertion(long_str, lat_str)
            after_location = (converted_location.lat, converted_location.long)
            
            distance = 0
            try:
                distance = dis.distance(before_location, after_location)
            except ValueError as error:
                print('Something went wrong: ({}, {}) | ({}, {})'.format(long_str, lat_str, converted_location.long_str, converted_location.lat_str))
                print(error)

            print('({}, {})  |  ({}, {}  | distance: {})'.format(long_str, lat_str, converted_location.long, converted_location.lat, distance))

def get_location_after_convertion(long_str, lat_str):
    long_int_part = long_str.split('.')[0]
    long_decimal_part = long_str.split('.')[1]
    long_decimal_len = len(long_decimal_part)

    lat_int_part = lat_str.split('.')[0]
    lat_decimal_part = lat_str.split('.')[1]
    lat_decimal_len = len(lat_decimal_part)
    
    target_long_decimal_len = long_decimal_len
    if long_decimal_len > 3:
        target_long_decimal_len = 3 #long_decimal_len - 1
    
    target_lat_decimal_len = lat_decimal_len
    if lat_decimal_len > 3:
        target_lat_decimal_len = 3 #lat_decimal_len - 1
    
    target_long_decimal_part = long_decimal_part[0:target_long_decimal_len]
    target_lat_decimal_part = lat_decimal_part[0:target_lat_decimal_len]

    converted_long_str = long_int_part + '.' + target_long_decimal_part
    converted_lat_str = lat_int_part + '.' + target_lat_decimal_part

    converted_long = float(converted_long_str)
    converted_lat = float(converted_lat_str)

    return Location(converted_long, converted_lat, converted_long_str, converted_lat_str)

class Location(object):
    
    long = 0
    lat = 0 
    long_str = ''
    lat_str = ''

    def __init__(self, long, lat, long_str, lat_str):
        self.long = long
        self.lat = lat
        self.long_str = long_str
        self.lat_str = lat_str


if __name__ == '__main__':
    check_arg()
    read_file_and_calculate(sys.argv[1])