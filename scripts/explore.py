#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import csv
from geopy import distance as dis

def check_arg():
    if len(sys.argv) != 2:
        print('Invalid command line input! Your input should be something like \
        python explore.py path_to_file')

def extract_csv_lines_from(file_path):

    """Extract lines fron the given file. Essentially every line is a combination of timestamp and longitute and latitude
    """

    csv_lines = []
    with open(file_path, 'r') as file:
        for line in file:
            data = line.split('\t')
            
            time_str = data[0].strip()
            long_str = data[1].strip()
            lat_str = data[2].strip()

            csv_lines.append(CsvLine(time_str, long_str, lat_str))

    return csv_lines


def write_csv_lines_to_csv(file_path):
    csv_lines = extract_csv_lines_from(file_path)
    csv_file_path = file_path + '.csv'
    with open(csv_file_path, 'w', newline='') as file:
        field_names = ['datetime', 'longitude', 'long_decimal_len', 'latitude', 'lat_decimal_len']
        writer = csv.DictWriter(file, fieldnames=field_names)
        for csv_line in csv_lines:
            long_decimal_len = get_decimal_len_from_str(csv_line.long_str)
            lat_decimal_len = get_decimal_len_from_str(csv_line.lat_str)
            writer.writerow(
            {'datetime': csv_line.time_str, 
            'longitude': csv_line.long_str, 
            'long_decimal_len': str(long_decimal_len), 
            'latitude': csv_line.lat_str, 
            'lat_decimal_len': str(lat_decimal_len)
            })


def get_decimal_len_from_str(long_lat_titude):
    return len(long_lat_titude.split('.')[1])
    


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

class CsvLine(object):

    time_str = ''
    long_str = ''
    lat_str = ''

    def __init__(self, time_str, long_str, lat_str):
        self.time_str = time_str
        self.long_str = long_str
        self.lat_str = lat_str

if __name__ == '__main__':
    check_arg()
    write_csv_lines_to_csv(sys.argv[1])
    