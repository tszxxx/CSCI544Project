import csv
import os

def get_text_to_audio(audio_file_path, input_file_path, output_file_path):
    audio_dict = {}
    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        spamreader = csv.reader(input_file, delimiter=',', quotechar='\"')
        cnt = 0
        for record in spamreader:
            if cnt > 0:
                id = record[0]
                score = record[6]
                a, b = divmod(cnt, 4)
                audio_dict[id] = {'score': score, 'index': b}
            cnt += 1
    with open(audio_file_path, 'r') as audio_file:
        with open(output_file_path, 'w') as output_file:
            cnt = 0
            segmentations_dirs = ['char_data', 'jieba_data', 'pku_data', 'snlp_data']
            spamreader = csv.reader(audio_file, delimiter=',', quotechar='\"')
            output_file.write('id,audio_path,char_path,jieba_path,pku_path,snlp_path\n')
            for record in spamreader:
                if cnt > 0:
                    id = record[0].split('.')[0]
                    score = audio_dict[id]['score']
                    index = audio_dict[id]['index']
                    output_file.write(id + ',' + 'Audio_Data/' + record[0])
                    for root_dir in segmentations_dirs:
                        file_path = root_dir + '/' + str(index) + '/' + score + '-' + id + '.txt'
                        output_file.write(',' + file_path)
                    output_file.write('\n')
                    print(cnt)
                cnt += 1


if __name__ == '__main__':
    audio_file_path = '../Audio_Data.csv'
    input_file_path = '../Movie_information.csv'
    output_file_path = '../Text_To_Audio.csv'
    get_text_to_audio(audio_file_path, input_file_path, output_file_path)