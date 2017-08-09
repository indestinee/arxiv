from lib.spider import *
import time

def init():
    try:
        with open(checkpoint, 'r') as f:
            lastest = f.readlines()[-1][:-1]
        with open(lastest, 'rb') as f:
            return pickle.load(f), True
    except:
        return {'arxiv_id': {}, 'author': {}, 'time': {}, 'title': {}}, False

def save(data):
    data_base_path = 'data/%d.pkl' % int(time.time())
    with open(data_base_path, 'wb') as f:
        pickle.dump(data, f)
    with open(checkpoint, 'a') as f:
        f.write('%s\n' % data_base_path)

def fetch():
    import os
    os.system('./download.sh')

def download_pdf(url, download_all):
    print(url)
    return False


def download(download_all = False):
    for each, value in data_base['arxiv_id'].items():
        if value['succeed'] and not value['download']:
            value['download'] = download_pdf(value['pdf'], download_all)
