#coding=utf8
import jieba
from urllib import request, parse
import sys
import json
import os
from ThirdParty_langconv import *
import stanfordnlp
import pkuseg
import re

stopwords = [word.strip() for word in open('../Original_Files/stopwords.txt', encoding='utf-8')]

def pku_segmentation(sentence, tokenizer):
    global stopwords
    return [word for word in tokenizer.cut(sentence) if (len(word)>0 and word not in stopwords)]

def character_segmentation(sentence):
    global stopwords
    pattern = re.compile(r'([\u4e00-\u9fa5])')
    character_seg_list = pattern.split(sentence.strip())
    def extract_info(c):
        if (len(c)) == 0:
            return ''
        seg_list = re.findall(r'[0-9]+', c).append(re.findall(r'[a-zA-Z]+', c))
        if seg_list is None:
            return ''
        return [seg for seg in seg_list if seg not in stopwords]

    char_list = [char if (re.match(r'^[\u4e00-\u9fa5]$', char) is not None and char not in stopwords) else extract_info(char) for char in character_seg_list]
    return [char for char in char_list if len(char)>0]

def stanford_segmentation(sentence, tokenizer):
    global stopwords
    token_stanford = []

    token_list = tokenizer(sentence)
    for sent in token_list.sentences:
        for word in sent.words:
            if word.lemma not in stopwords and not re.search(r'[^\w\s\u4e00-\u9fa5]',word.lemma):
                token_stanford.append(word.lemma)
    return token_stanford

def convert_simplified_Chinese(sentence):
    sentence = Converter('zh-hans').convert(sentence)
    return sentence

def process_input(input_file_path, output_dir):
    global stopwords
    cnt = 0
    input_file = open(input_file_path, 'r', encoding='UTF-8')
    stanford_tokenizer = stanfordnlp.Pipeline(processors='tokenize,lemma', lang='zh', models_dir='/Users/hangjiezheng/Desktop/CSCI534')
    pku_tokenizer = pkuseg.pkuseg(model_name='web')
    for line in input_file:
        if cnt == 0:
            cnt += 1
        else:
            tokens = line.split('\t')

            output_file_path = [dir + '/' + tokens[6] + '-' + tokens[0] + '.txt' for dir in output_dir]
            output_files = [open(file_path, 'w', encoding='UTF-8') for file_path in output_file_path]

            for index in range(1, 6):
                text = convert_simplified_Chinese(tokens[index])

                # jieba segmentation
                seg_list = jieba.cut(text, cut_all=False)
                for seg in seg_list:
                    if seg not in stopwords:
                        output_files[0].write(seg + ' ')
                
                text = re.sub('[（）]', '', text)
                # character segmentation
                character_seg = character_segmentation(text)
                output_files[1].write(' '.join(character_seg))
                output_files[1].write(' ')

                # stanfordnlp segmentation
                stanford_seg = stanford_segmentation(text, stanford_tokenizer)
                output_files[2].write(' '.join(stanford_seg))
                output_files[2].write(' ')
                
                # pkuseg segmentation
                pku_seg = pku_segmentation(text, pku_tokenizer)
                output_files[3].write(' '.join(pku_seg))
                output_files[3].write(' ')

            [output_file.close() for output_file in output_files]
        
if __name__ == '__main__':
    input_file_path = '../Movie_information.txt'
    output_dir = ['../jieba_data', '../char_data', '../snlp_data', '../pku_data']
    for dir in output_dir:
        if not os.path.exists(dir):
            os.mkdir(dir)
    process_input(input_file_path, output_dir)