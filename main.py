from IPython import embed
from argparse import ArgumentParser
from lib import *

def check_args():
    parser = ArgumentParser()
    parser.add_argument('--order', default='cmd', choices=['cmd', 'update', 'download', 'fetch'])
    return parser.parse_args()


if __name__ == '__main__':
    args = check_args()

    data_base, loaded = init()
    if not loaded:
        print('[WRN] Database is empty! Update first..')
    if args.order == 'cmd':
        print('[WRN] Don\'t forget to save after update..')
        embed()
    elif args.order == 'update':
        update(data_base)
        save(data_base)
    elif args.order == 'download':
        download(data_base)
    elif args.order == 'fetch':
        fetch()
