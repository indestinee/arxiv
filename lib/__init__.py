from lib import spider
import pickle, time, os
preffix = 'https://arxiv.org/'

checkpoint = 'checkpoint.txt'

def clear():
    os.system('rm data/* pdf/* checkpoint.txt')

def init():
    os.chdir(os.path.realpath('.'))
    if not os.path.isdir('data'):
        os.mkdir('data')
    if not os.path.isdir('pdf'):
        os.mkdir('pdf')

    try:
        with open(checkpoint, 'r') as f:
            lastest = f.readlines()[-1][:-1]
        with open(lastest, 'rb') as f:
            data_base = pickle.load(f)
    except:
        data_base = {'arxiv_id': {}, 'author': {}, 'time': {}, 'title': {}}
    return data_base

data_base = init()

def save():
    data_base_path = 'data/%d.pkl' % int(time.time())
    with open(data_base_path, 'wb') as f:
        pickle.dump(data_base, f)
    with open(checkpoint, 'a') as f:
        f.write('%s\n' % data_base_path)


def fetch():
    os.system('rsync -avz $sdo:~/Github/arxiv/pdf/* ./pdf/')
    os.system('rsync -avz $sdo:~/Github/arxiv/data/* ./data/')
    os.system('rsync -avz $sdo:~/Github/arxiv/checkpoint.txt ./')


def file_name(arxiv_id):
    if arxiv_id in data_base['arxiv_id']:
        return 'data/' + (arxiv_id + '::' + data_base['arxiv_id'][arxiv_id]['title']).replace(' ', '_')
    return ''

def download_pdf(arxiv_id, url=''):
    if url == '':
        url = preffix + 'pdf/' + arxiv_id
    try:
        name = file_name(arxiv_id)
        data = spider.reach_url(url)
        with open(name, 'wb') as f:
            f.write(data)
        return True, name
    except:
        return False, ''


def download(download_all = False):
    for each, value in data_base['arxiv_id'].items():
        if value['succeed'] and (download_all or not value['download']):
            value['download'], value['file'] = download_pdf(each, value['pdf'])
    print('[WRN] Don\'t forget to save after operation..')


def update(update_all = True):
    remain, totle = spider.update(data_base, update_all)
    print('Need to fetch %d, fetched %d in fact..' % (totle, remain))
    print('[WRN] Don\'t forget to save after operation..')

def show(result_list, ignore = {'abstract'}):
    for each in result_list:
        data = data_base['arxiv_id'][each]
        print('>>>>\narxiv_id: ', each)
        for key, value in data.items():
            if key in ignore:
                continue
            print('    {}: {}'.format(key, value))
        print('<<<<\n')

def search(arxiv_id, show__ = False, ignore = {'abstract'}):
    result_list = []
    for key, value in data_base.items():
        if key == 'arxiv_id':
            if arxiv_id in value.keys():
                result_list.append(arxiv_id)
        else:
            if arxiv_id in value:
                data = value[arxiv_id]
                if type(data) == str:
                    result_list.append(arxiv_id)
                if type(data) == list:
                    for every in data:
                        result_list += data
    if show__:
        show(result_list, ignore)
    return result_list




