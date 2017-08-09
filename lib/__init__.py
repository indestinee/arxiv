from lib.spider import *
import pickle, time, os

def clear():
    os.system('rm data/* pdf/* checkpoint.txt')

def init():
    os.chdir(os.path.realpath('.'))
    if not os.path.isdir('data'):
        os.mkdir('data')
    if not os.path.isdir('pdf'):
        os.mkdir('pdf')
    try:
        with open('checkpoint.txt', 'r') as f:
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
    os.system('rsync -avz $sdo:~/Github/arxiv/pdf/* ./pdf/')
    os.system('rsync -avz $sdo:~/Github/arxiv/data/* ./data/')
    os.system('rsync -avz $sdo:~/Github/arxiv/checkpoint.txt ./')

def download_pdf(url):
    print(url)
    return False


def download(download_all = False):
    for each, value in data_base['arxiv_id'].items():
        if value['succeed'] and (download_all or not value['download']):
            value['download'] = download_pdf(value['pdf'], download_all)
    print('[WRN] Don\'t forget to save after update..')


def update(data_base, update_all = True):
    remain, totle = __update(data_base, update_all)
    print('Need to fetch %d, fetched %d in fact..' % (totle, remain))
    print('[WRN] Don\'t forget to save after update..')
