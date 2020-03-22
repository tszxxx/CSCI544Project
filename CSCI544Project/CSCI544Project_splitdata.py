import json
import os
import sys
import string
import re

zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
cnt = 0

def output_header(output_file):
    output_file.write('id\t')
    output_file.write('电影名\t')
    output_file.write('内容简介\t')
    output_file.write('主演\t')
    output_file.write('导演\t')
    output_file.write('编剧\t')
    output_file.write('评分\t')
    output_file.write('预告片URL\n')

def fetchData(file_path, output_file):
    input_file = open(file_path, 'r', encoding='UTF-8')
    line = input_file.readline()
    tmp = json.loads(line)
    global zh_pattern, cnt
    if len(tmp['trailer_urls']) > 0 and len(tmp['aka']) > 0 and len(tmp['directors']) > 0 and len(tmp['writers']) > 0 and len(tmp['casts']) > 2:
        if tmp['rating']['average'] > 0 and (tmp['rating']['average'] < 4 or tmp['rating']['average'] > 6):
            output_file.write(tmp['id'] + '\t')
            if zh_pattern.search(tmp['original_title']):
                output_file.write(tmp['original_title'] + '\t')
            else:
                output_file.write(tmp['aka'][0] + '\t')
            output_file.write(tmp['summary'].replace('\n','') + '\t')
            output_file.write(tmp['casts'][0]['name'] + ',' + tmp['casts'][1]['name'] + ',' + tmp['casts'][2]['name'] + '\t')
            output_file.write(tmp['directors'][0]['name'] + '\t')
            output_file.write(tmp['writers'][0]['name'] + '\t')
            output_file.write(str(tmp['rating']['average']) + '\t')
            output_file.write(tmp['trailer_urls'][0] + '\n')
            cnt += 1
            print(cnt)

if __name__ == '__main__':
    dir = '../Raw_Information'
    output_file_path = '../Movie_information.txt'
    output_file = open(output_file_path, 'w', encoding='UTF-8')
    output_header(output_file)
    for root,dirs,files in os.walk(dir):
        for file in files:
            file_path = os.path.join(root,file)
            fetchData(file_path, output_file)

    output_file.close()
