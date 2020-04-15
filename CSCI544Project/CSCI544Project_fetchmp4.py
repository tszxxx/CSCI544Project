import os
import requests
import csv

def fetchMP4(input_file_path, output_file_dir, special_list=None):
    output_file_dir += '/'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
    }
    with open(input_file_path, 'r', encoding='UTF-8') as input_file:
        spamreader = csv.reader(input_file, delimiter=',', quotechar='\"')
        cnt = 0
        for record in spamreader:
            if cnt > 0:
                if len(record[-1]) > 0:
                    url = record[-1]
                    id = record[0]
                    if special_list is None or id in special_list:
                        response = requests.get(url, headers=header)
                        output_file = open(output_file_dir + id + '.mp4', 'wb')
                        if len(response.content) == 0:
                            print(id)
                        output_file.write(response.content)
                        output_file.close()
                print(cnt, end='\r')
            cnt += 1

if __name__ == '__main__':
    input_file_path = '../Movie_information.csv'
    output_file_dir = '../Audio_Data'
    if not os.path.exists(output_file_dir):
        os.mkdir(output_file_dir)
    fetchMP4(input_file_path, output_file_dir, None) #['1947335'])

