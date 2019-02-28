import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_file_path = BASE_DIR + '/data/'
infile_path = data_file_path + 'proxy.csv'
outfile_path = data_file_path + 'user_proxies.csv'


if __name__ == '__main__':
    print(BASE_DIR)
