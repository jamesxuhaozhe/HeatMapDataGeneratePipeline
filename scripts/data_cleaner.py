#!/usr/bin/env python
# -*- coding:utf-8 -*-

import csv
import os
import sys
import time
from datetime import datetime

# date time format
DATE_TIME_FORMAT = '%Y/%m/%d %H:%M:%S'

# all the available rent type
RENT_TYPE_SHARED_BIKE = 1
RENT_TYPE_ELECTRIC_MOPED = 8
RENT_TYPE_SHARED_CAR = 7
RENT_TYPE_PUBLIC_BIKE = 2

# file path for each rent type
PATH_TO_SHARED_BIKE = '/home/haozhexu/data/shared_bike.dat'
PATH_TO_ELECTRIC_MOPED = '/home/haozhexu/data/electric_moped.dat'
PATH_TO_SHARED_CAR = '/home/haozhexu/data/shared_car.dat'
PATH_TO_PUBLIC_BIKE = '/home/haozhexu/data/public_bike.dat'
PATH_TO_ALL_RENT_TYPE = '/home/haozhexu/data/all.dat'

def check_arg():
    if len(sys.argv) != 2:
        print("You need to specify the csv file source. Run it like the following \
        python data_cleaner.py path_to_your_csv_file")

def get_path_to_file():
    """
    return the path to the csv file
    """
    return sys.argv[1]

def read_csv_file_and_write_to_files():
    """
    read the csv file and then print each line to console
    """
    path_to_file = get_path_to_file()
    with open(path_to_file, newline='') as csvfile:

        shared_bike_lines_to_write = []
        electric_moped_lines_to_write = []
        shared_car_lines_to_write = []
        public_bike_lines_to_write = []

        reader = csv.DictReader(csvfile)
        for row in reader:

            lend_time = get_datetime_from_string_csv_field(row['lend_time'])
            rent_long = get_float_number_from_string_csv_field(row['rent_long'])
            rent_lat = get_float_number_from_string_csv_field(row['rent_lat'])         
            bike_type = int(row['bike_type'])

            if check_valid_rent_long_and_rent_lat(rent_long, rent_lat) and check_valid_rent_type(bike_type):
                line_to_append = str(lend_time) + '\t' + str(rent_long) + '\t' + str(rent_lat)
                if bike_type == RENT_TYPE_SHARED_BIKE:
                    shared_bike_lines_to_write.append(line_to_append)
                elif bike_type == RENT_TYPE_ELECTRIC_MOPED:
                    electric_moped_lines_to_write.append(line_to_append)
                elif bike_type == RENT_TYPE_SHARED_CAR:
                    shared_car_lines_to_write.append(line_to_append)
                elif bike_type == RENT_TYPE_PUBLIC_BIKE:
                    public_bike_lines_to_write.append(line_to_append)

        print('write file into: {}'.format(PATH_TO_SHARED_BIKE))
        write_to_file(PATH_TO_SHARED_BIKE, shared_bike_lines_to_write)

        print('write file into: {}'.format(PATH_TO_ELECTRIC_MOPED))
        write_to_file(PATH_TO_ELECTRIC_MOPED, electric_moped_lines_to_write)

        print('write file into: {}'.format(PATH_TO_SHARED_CAR))
        write_to_file(PATH_TO_SHARED_CAR, shared_car_lines_to_write)

        print('write file into: {}'.format(PATH_TO_PUBLIC_BIKE))
        write_to_file(PATH_TO_PUBLIC_BIKE, public_bike_lines_to_write)

        print('write file into: {}'.format(PATH_TO_ALL_RENT_TYPE))
        write_to_file(PATH_TO_ALL_RENT_TYPE, shared_bike_lines_to_write 
        + electric_moped_lines_to_write
         + shared_car_lines_to_write
          + public_bike_lines_to_write)
                
def get_float_number_from_string_csv_field(string_field_csv):
    """convert the raw field from csv file to float type, in case the field is 
    empty, just assign 0 
    """
    if string_field_csv == '':
        return 0
    else:
        return float(string_field_csv)

def get_datetime_from_string_csv_field(string_field_csv):
    """convert the raw field from csv file to datetime type.
    one example of the date fime from csv file is "2018/12/2 12:54:34"
    """
    return datetime.strptime(string_field_csv, DATE_TIME_FORMAT)

def check_valid_rent_type(rent_type):
    """check if the given rent_type falls into the pre-defined rent type set
    """
    valid_rent_types = {RENT_TYPE_ELECTRIC_MOPED, RENT_TYPE_PUBLIC_BIKE, RENT_TYPE_SHARED_BIKE, RENT_TYPE_SHARED_CAR}
    return rent_type in valid_rent_types

def check_valid_rent_long_and_rent_lat(rent_long, rent_lat):
    """checks if any given long or lat is 0 or not.
    A valid (long, lat) should be (long>0, lat>0) return false if not valid
    """
    return not(rent_long == 0 or rent_lat == 0)

def write_to_file(file_path, contents):
    """create a file based on the file path if it does not exist yet.
    delete the file if it has already exists and then create a new one.
    """   
    try:
        if os.path.exists(file_path):
            os.remove(file_path)

        with open(file_path, 'w+') as file:
            if contents:
                file.write('\n'.join(contents))
    except FileNotFoundError:
        print('Something went wrong when creating: {}'.format(file_path))

if __name__ == '__main__':
    check_arg()
    read_csv_file_and_write_to_files()
    