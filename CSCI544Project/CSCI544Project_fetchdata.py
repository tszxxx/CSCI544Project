import json
import os
import sys
import urllib.request

def get_preprocess(input_file_path):
    file = open(input_file_path, 'r')
    id_list = []
    for line in file:
        id_list.append(line)
    file.close()
    return id_list
        
def fetch_data(id):
    try:
        url = 'https://douban.uieee.com/v2/movie/subject/'+id
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
        }
        request = urllib.request.Request(url, headers=header)
        reponse = urllib.request.urlopen(request).read()
        tmp = json.loads(reponse)
        return tmp
    except BaseException as e:
        return None

def get_output(file_path, tmp):
    output_file = open(file_path, 'w', encoding='UTF-8')
    output_file.write(json.dumps(tmp))
    output_file.close()

if __name__ == '__main__':
    cnt = 0
    input_file_path = '../Movie_Links/movie_links.txt'
    error_file_path = '../Movie_Links/movie_links_errors.txt'
    output_dir_path = '../Raw_Information'
    if not os.path.exists(output_dir_path):
        os.mkdir(output_dir_path)
    id_list = get_preprocess(input_file_path)
    with open(error_file_path, 'w') as error_file:
        for index, id in enumerate(id_list):
            id = id.strip('\n')
            file_path = output_dir_path + '/' + id + '.txt'
            cnt += 1
            if not os.path.exists(file_path):
                tmp = fetch_data(id)
                if tmp is not None:
                    get_output(file_path, tmp)
                    print(cnt)
                else:
                    error_file.write(id + '\n');
                    print(cnt, id, 'error')

