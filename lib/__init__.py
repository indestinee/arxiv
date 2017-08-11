from lib import spider
import pickle, time, os, threading, queue
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


def fetch(l = [], use_all = False):
    if use_all:
        os.system('rsync -avz $sdo:~/Github/arxiv/pdf/* ./pdf/')
    else:
        ll = [l] if type(l) != list else l
        
        for each in ll:
            cmd = 'rsync -avz $sdo:~/Github/arxiv/pdf/%s ./pdf/' % each.replace(' ', '_')
            print('--------\n>>>>  %s\n--------' % cmd)
            os.system(cmd)

    cmd = 'rsync -avz $sdo:~/Github/arxiv/data/* ./data/'
    print('--------\n>>>>  %s\n--------' % cmd)
    os.system(cmd)

    cmd = 'rsync -avz $sdo:~/Github/arxiv/checkpoint.txt ./'
    print('--------\n>>>>  %s\n--------' % cmd)
    os.system(cmd)


def file_name(arxiv_id):
    if arxiv_id in data_base['arxiv_id']:
        return 'pdf/' + (arxiv_id + '::' + data_base['arxiv_id'][arxiv_id]['title'] + '.pdf').replace(' ', '_')
    return ''

def download_pdf(arxiv_id, url=''):
    if url == '':
        url = preffix + 'pdf/' + arxiv_id
    try:
        name = file_name(arxiv_id)
        data = spider.reach_url(url).content
        with open(name, 'wb') as f:
            f.write(data)
        return True, name
    except:
        return False, ''

share = queue.Queue(-1)

def download_list(l, step, first, num):
    for i in range(first, num, step):
        flag, file_name = download_pdf(l[i])
        share.put([flag, l[i][0], file_name])
    share.put([-1])
    #value['download'], value['file'] = download_pdf(each, value['pdf'])

thread_num = 8

def __download(q):
    t = []
    num = len(q)
    for i in range(thread_num):
        t.append(threading.Thread(target=download_list, args=(q, thread_num, i, num)))
    for i in t:
        i.start()
    cnt = thread_num
    done = 0
    while cnt > 0:
        data = share.get()
        if data[0] == -1:
            cnt -= 1
        else:
            print(data)
            if data[0]:
                data_base['arxiv_id'][data[1]]['download'] = True
                data_base['arxiv_id'][data[1]]['file'] = data[2]
            done += 1
            print('Done %d/%d %s..' % (done, num, 'succeed' if data[0] else 'fail'))
    print('[WRN] Don\'t forget to save after operation..')

def download(l = []):
    q = []
    if len(l) == 0:
        for each, value in data_base['arxiv_id'].items():
            if value['succeed'] and not value['download']:
                q.append(each)
        __download(q)
    else:
        __download(l)


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



if __name__ == '__main__':
    __download([str(i) for i in range(20)])
