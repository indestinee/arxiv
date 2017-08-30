from IPython import embed
from argparse import ArgumentParser
from lib import *

def check_args():
    parser = ArgumentParser()
    parser.add_argument('-m', '--mode', default='cmd', choices=['cmd', 'update', 'download', 'fetch', 'clear'])
    return parser.parse_args()




if __name__ == '__main__':
    args = check_args()

    if len(data_base['arxiv_id']) == 0:
        print('[WRN] Database is empty! Update first..')


    if args.mode == 'cmd':
        print('[WRN] Don\'t forget to save after operation..')
        embed()
    elif args.mode == 'update':
        update()
        save()
    elif args.mode == 'download':
        download()
    elif args.mode == 'fetch':
        fetch()
    elif args.mode == 'clear':
        clear()
    elif args.mode == 'auto':
        while True:
            update()
            save()
            data_base = init()
            time.sleep(86400)


