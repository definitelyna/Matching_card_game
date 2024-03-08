import csv, os

def get_csv():
    list_of_files = os.listdir()
    csv_file_arr = []
    for csv_file in list_of_files:
        if csv_file.split(".")[-1] == "csv":
            csv_file_arr.append(csv_file)

    return csv_file_arr[0]

def import_file():

    file_name = get_csv()
    question_dict = {}
    csv_file = open(file_name , "r")
    csvreader = csv.reader(csv_file)
    for row in csvreader:
        question_dict[row[0]] = row[1]
    return question_dict

