import csv
import shutil
import os

def train_test_split(input_file_path, input_dir):
    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        spamreader = csv.reader(input_file, delimiter=',', quotechar='\"')
        cnt = 0
        for record in spamreader:
            if cnt > 0:
                for dir in input_dir:
                    source_file_path = dir + '/' + record[6] + '-' + record[0] + '.txt'
                    a, b = divmod(cnt, 4)
                    if not os.path.exists(dir + '/' + str(b)):
                        os.mkdir(dir + '/' + str(b))
                    target_file_path = dir + '/' + str(b) + '/' + record[6] + '-' + record[0] + '.txt'
                    shutil.move(source_file_path, target_file_path)
                print(cnt)
            cnt += 1

if __name__ == '__main__':
    input_file_path = '../Movie_information.csv'
    input_dir = ['../jieba_data', '../char_data', '../snlp_data', '../pku_data']
    train_test_split(input_file_path, input_dir)
