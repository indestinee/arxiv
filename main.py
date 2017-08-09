from IPython import embed
from argparse import ArgumentParser
from lib import *

def check_args():
    parser = ArgumentParser()
    parser.add_argument('-m', '--mode', default='cmd', choices=['cmd', 'update', 'download', 'fetch', 'clear'])
    return parser.parse_args()


if __name__ == '__main__':
    args = check_args()

    data_base, loaded = init()
    if not loaded:
        print('[WRN] Database is empty! Update first..')
    if args.mode == 'cmd':
        print('[WRN] Don\'t forget to save after update..')
        embed()
    elif args.mode == 'update':
        update(data_base)
        save(data_base)
    elif args.mode == 'download':
        download(data_base)
    elif args.mode == 'fetch':
        fetch()
    elif args.mode == 'clear':
        clear()
