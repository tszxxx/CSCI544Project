import os
import requests
import csv

def fetchMP4(input_file_path, output_file_dir):
    output_file_dir += '/'
    with open(input_file_path, 'r', encoding='UTF-8') as input_file:
        spamreader = csv.reader(input_file, delimiter=',', quotechar='\"')
        cnt = 0
        for record in spamreader:
            if cnt > 0:
                if len(record[-1]) > 0:
                    url = record[-1]
                    id = record[0]
                    response = requests.get(url)
                    output_file = open(output_file_dir + id + '.mp4', 'wb')
                    output_file.write(response.content)
                    output_file.close()
                print(cnt)
            cnt += 1

if __name__ == '__main__':
    input_file_path = '../Movie_information.csv'
    output_file_dir = '../Audio_Data'
    if not os.path.exists(output_file_dir):
        os.mkdir(output_file_dir)
    fetchMP4(input_file_path, output_file_dir)

