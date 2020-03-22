import sys
import os
import random
import re
from collections import defaultdict

cnt = 0

def process_file(input_file_path, output_file):
    global cnt
    if input_file_path.find('.txt') != -1 and input_file_path.find('stopwords') == -1:
        file = open(input_file_path, 'r', encoding='UTF-8')
        for line in file:
            tokens = line.split()
            for token in tokens:
                res = re.search(r'href="https://movie.douban.com/subject/(\d+)/"', token)
                if res != None:
                    output_file.write(res.group(1) + '\n')
                    cnt += 1
                    print(cnt)
        file.close()
        

if __name__ == '__main__':
    movie_dir_path = '../Movie_Links'
    if not os.path.exists(movie_dir_path):
        os.mkdir(movie_dir_path)
    output_file_path = movie_dir_path + '/' + 'movie_links.txt'
    output_file = open(output_file_path,'w')
    for root,dirs,files in os.walk('../Original_Files'):
        for file in files:
            file_path = os.path.join(root,file)
            process_file(file_path, output_file)
    output_file.close()

