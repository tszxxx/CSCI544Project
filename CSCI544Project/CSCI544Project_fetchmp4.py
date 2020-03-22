import json
import os
import sys
import requests

def fetchMP4(file_path, dir):
    file = open(file_path, 'r', encoding='UTF-8')
    cnt = 0
    for line in file:
        if cnt == 0:
            cnt += 1
        else:
            tokens = line.split('\t')
            url = tokens[-1]
            id = tokens[0]
            response = requests.get(url)
            output_file = open(dir + '/' + id + '.mp4', 'wb')
            output_file.write(response.content)
            output_file.close()

if __name__ == '__main__':
    print('input your part from 0 to 3')
    operator = sys.stdin.readline()
    operator = int(operator[0])
    dir = 'mp4'+str(operator)
    if not os.path.exists(dir):
        os.mkdir(dir)
    input_file_path = 'information'+str(operator)+'.tt'
    fetchMP4(input_file_path, dir)

