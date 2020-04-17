import os
import csv
import math
def getScoreDist(input_file_path, output_file_dir):
    if not os.path.exists(output_file_dir):
        os.mkdir(output_file_dir)
    output_file_dir += '/'
    output_file_path = output_file_dir + 'score_distribution.csv'
    if not os.path.exists(output_file_path):
        score_dict = {}
        with open(input_file_path, 'r', encoding='UTF-8') as input_file:
            spamreader = csv.reader(input_file, delimiter=',', quotechar='\"')
            cnt = 0
            for record in spamreader:
                if cnt > 0:
                    score = math.floor(float(record[6].strip()))
                    score_dict[score] = score_dict.get(score, 0) + 1
                    print(cnt)
                cnt += 1
        with open(output_file_path, 'w') as output_file:
            output_file.write('score,count\n')
            for key in range(0, 10):
                output_file.write(str(key) + ',' + str(score_dict.get(key, 0)) + '\n')

def getSegmentationDist(input_file_path, output_file_dir):
    if not os.path.exists(output_file_dir):
        os.mkdir(output_file_dir)
    output_file_dir += '/'
    segmentation_dict = {'char_data':{}, 'jieba_data':{}, 'pku_data':{}, 'snlp_data':{}}
    segmentations = ['char_data', 'jieba_data', 'pku_data', 'snlp_data']
    with open(input_file_path, 'r', encoding='UTF-8') as input_file:
        spamreader = csv.reader(input_file, delimiter=',', quotechar='\"')
        cnt = 0
        for record in spamreader:
            if cnt > 0:
                id = record[0]
                score = record[6]
                for root_dir in segmentations:
                    a, b = divmod(cnt, 4)
                    file_path = '../' + root_dir + '/' + str(b) + '/' + score + '-' + id + '.txt'
                    word_cnt = 0
                    with open(file_path, 'r', encoding='utf-8') as file:
                        for line in file:
                            word_cnt += len(line.strip().split(' '))
                    segmentation_dict[root_dir][word_cnt] = segmentation_dict[root_dir].get(word_cnt, 0) + 1
                print(cnt)
            cnt += 1
    for root_dir in segmentations:
        output_file_path = output_file_dir + root_dir + '_segmentation_distribution.csv'
        with open(output_file_path, 'w') as output_file:
            output_file.write('words,count\n')
            for key in segmentation_dict[root_dir]:
                output_file.write(str(key) + ',' + str(segmentation_dict[root_dir][key]) + '\n')

if __name__ == '__main__':
    input_file_path = '../Movie_information.csv'
    output_file_dir = '../Statistical_Results'
    getScoreDist(input_file_path, output_file_dir)
    getSegmentationDist(input_file_path, output_file_dir)