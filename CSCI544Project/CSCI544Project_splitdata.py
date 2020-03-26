import json
import os
import sys
import string
import csv
import re

zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
cnt = 0

def output_header(spamwriter):
    spamwriter.writerow(['id', '电影名', '内容简介', '主演', '导演', '编剧', '评分', '预告片URL'])

def get_arr_value(arr, key, max_num=None):
    if max_num is None:
        max_num = len(arr)
    try:
        ret = []
        for item in arr[:max_num]:
            if key is not None:
                ret.append(item[key])
            else:
                ret.append(item)
        return ret
    except BaseException as e:
        return []

def fetchData(file_path, spamwriter):
    input_file = open(file_path, 'r', encoding='UTF-8')
    line = input_file.readline()
    tmp = json.loads(line)
    global zh_pattern, cnt
    if len(tmp['summary']) > 0:
        row = []
        row.append(tmp['id'])
        if zh_pattern.search(tmp['original_title']):
            row.append(tmp['original_title'])
        else:
            isFound = False
            for title in tmp['aka']:
                if zh_pattern.search(title):
                    row.append(title)
                    isFound = True
                    break
            if isFound is not True:
                if len(tmp['aka']) > 0:
                    row.append(tmp['aka'][0])
                else:
                    row.append(tmp['original_title'])

        row.append(tmp['summary'].replace('\r', ' ').replace('\n', ' ').replace('  ', ' '))

        row.append(','.join(get_arr_value(tmp['casts'], 'name')))
        row.append(','.join(get_arr_value(tmp['directors'], 'name')))
        row.append(','.join(get_arr_value(tmp['writers'], 'name')))
        row.append(str(tmp['rating']['average']))
        row.append(','.join(get_arr_value(tmp['trailer_urls'], None, 1)))
        spamwriter.writerow(row)
    cnt += 1
    print(cnt)

if __name__ == '__main__':
    dir = '../Raw_Information'
    output_file_path = '../Movie_information.csv'
    output_file = open(output_file_path, 'w', encoding='UTF-8')
    spamwriter = csv.writer(output_file, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
    output_header(spamwriter)
    for root,dirs,files in os.walk(dir):
        for file in files:
            file_path = os.path.join(root,file)
            fetchData(file_path, spamwriter)

    output_file.close()
