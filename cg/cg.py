#coding: utf-8
from .logx import setup_logging
import logging
import argparse
import sys
import os
# don`t remove this line
setup_logging()
logger = logging.getLogger(__name__)
from os.path import join, isfile



def feed(src,dest):
    replacement = """some
    multi-line string"""

    for dname, dirs, files in os.walk(src,topdown=False):
        print(dname, dirs, files)
        # continue

        # rename folder 
        destfolder = join("/".join(dname.split("/")[:-1]),dest)
        os.rename(dname,destfolder)
        for filename in files:
            oldfile = join(destfolder,src)
            if isfile(oldfile):
                os.rename(oldfile,join(destfolder,dest))

        # rename file
        # replace filecontent
        # for fname in files:
            # fpath = os.path.join(dname, fname)
            # with open(fpath) as f:
                # s = f.read()
            # s = s.replace("${replace}", replacement)
            # with open(fpath, "w+") as f:
                # f.write(s)
    return 2

def main(args):
    ret = feed(args.src,args.dest)
    logger.debug(f'feed({args.src})={ret}')

def entry_point():
    parser = createParse()
    mainArgs=parser.parse_args()
    main(mainArgs)

def createParse():
    parser = argparse.ArgumentParser( formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="")
    subparsers = parser.add_subparsers()
    eat_parser = subparsers.add_parser('eat',formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="",  help='sub command demo')
    eat_parser.add_argument('-s', '--src',type=str,required=False, help='src', default="")  
    eat_parser.add_argument('-d', '--dest',type=str,required=False, help='dest', default="")  
    eat_parser.add_argument('-t', '--test', help='test questions', default=False, action='store_true') 
    return parser
