#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import csv
import time
import os
from geopy import distance as dis
from datetime import datetime as dt

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

def check_arg():
    if len(sys.argv) != 3:
        print('Invalid command line input! Your input should be something like \
        python explore.py path_to_file target_directory')

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

def do_math_and_write_to_csv(source_file_path, target_dir):
    os.makedirs(target_dir)

    lines = extract_csv_line2_from_csv(source_file_path)
    
    result_map = {}
    days_to_loop = get_days_to_loop(lines)
    for day in range(1, days_to_loop + 1):
        os.makedirs(target_dir + '/' + str(day))
        result_map.setdefault(day, {})

    for line in lines:
        time = dt.strptime(line.time_str, DATE_TIME_FORMAT)

        day = time.date().day
        hour = time.hour
        minute = time.minute

        minute_catergory = get_catergory_from_minute(minute)
        data_to_append = Line_to_write(line.long_str, line.lat_str, line.long_len_str, line.lat_len_str)

        day_map = result_map[day]

        if hour not in day_map:
            day_map.setdefault(hour, {'20': [], '40': [], '60': []})
            if minute_catergory == '20':
                twenty_list = day_map[hour]['20']
                twenty_list.append(data_to_append)
            elif minute_catergory == '40':
                forty_list = day_map[hour]['40']
                forty_list.append(data_to_append)
            elif minute_catergory == '60':
                sixty_list = day_map[hour]['60']
                sixty_list.append(data_to_append)
        else:
            if minute_catergory == '20':
                twenty_list = day_map[hour]['20']
                twenty_list.append(data_to_append)
            elif minute_catergory == '40':
                forty_list = day_map[hour]['40']
                forty_list.append(data_to_append)
            elif minute_catergory == '60':
                sixty_list = day_map[hour]['60']
                sixty_list.append(data_to_append)

    for day, item in result_map.items():
        for hour, item1 in item.items():
            for minute_cat, content_list in item1.items():
                file_name = target_dir + '/' + str(day) + '/' + str(hour) + '_' + minute_cat + '_' + str(len(content_list)) + '.csv'
                write_csv_file(file_name, content_list)


def write_csv_file(file_name, content_list):
    with open(file_name, 'w', newline='') as file:
        field_names = ['longitude', 'latitude', 'long_len', 'lat_len']
        writer = csv.DictWriter(file, fieldnames=field_names)
        for content in content_list:
            writer.writerow({
                'longitude': content.long_str,
                'latitude': content.lat_str,
                'long_len': content.long_len_str, 
                'lat_len': content.lat_len_str
                })

def get_catergory_from_minute(minute):
    if minute >= 0 and minute <= 20:
        return '20'
    elif minute > 20 and minute <= 40:
        return '40'
    elif minute > 40 and minute <= 60:
        return '60'
    else:
        return '-1'

def get_days_to_loop(lines):
    datetimes = []
    for line in lines:
        datetimes.append(dt.strptime(line.time_str, DATE_TIME_FORMAT))
    
    day_max = -sys.maxsize -1 
    for datetime in datetimes:
        day = datetime.date().day
        if day >= day_max:
            day_max = day
    
    return day_max
    

def extract_csv_line2_from_csv(source_file_path):
    lines = []
    with open(source_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            lines.append(CsvLine2(
            row['datetime'], 
            row['longitude'], 
            row['long_decimal_len'], 
            row['latitude'],  
            row['lat_decimal_len']))

    return lines

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

class CsvLine2(object):

    time_str = ''
    long_str = ''
    lat_str = ''
    long_len_str = ''
    lat_len_str = ''

    def __init__(self, time_str, long_str, lat_str, long_len_str, lat_len_str):
        self.time_str = time_str
        self.long_str = long_str
        self.lat_str = lat_str
        self.long_len_str = long_len_str
        self.lat_len_str = lat_len_str

class Line_to_write(object):

    long_str = ''
    lat_str = ''
    long_len_str = ''
    lat_len_str = ''

    def __init__(self, long_str, lat_str, long_len_str, lat_len_str):
        self.long_str = long_str
        self.lat_str = lat_str
        self.long_len_str = long_len_str
        self.lat_len_str = lat_len_str

if __name__ == '__main__':
    check_arg()
    #write_csv_lines_to_csv(sys.argv[1])
    do_math_and_write_to_csv(sys.argv[1], sys.argv[2])

    