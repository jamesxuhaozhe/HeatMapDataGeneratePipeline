import csv
import sys

RENT_TYPE_SHARED_BIKE = 1
RENT_TYPE_ELECTRIC_MOPED = 8
RENT_TYPE_SHARED_CAR = 7
RENT_TYPE_PUBLIC_BIKE = 2

def check_arg():
    if len(sys.argv) != 2:
        print("You need to specify the csv file source. Run it like the following \
        python data_cleaner.py path_to_your_csv_file")

def get_path_to_file():
    """
    return the path to the csv file
    """
    return sys.argv[1]

def read_csv_file():
    """
    read the csv file and then print each line to console
    """
    path_to_file = get_path_to_file()
    with open(path_to_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        i = 1
        for row in reader:
            i += 1
            print(row)
        print("Total number of lines is: " + str(i))

if __name__ == '__main__':
    check_arg()
    read_csv_file()