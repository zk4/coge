#coding: utf-8
from .logx import setup_logging
import logging
import argparse
import sys
import os
# don`t remove this line
setup_logging()
logger = logging.getLogger(__name__)
from os.path import join, isfile,basename
from pathlib import Path



def fullReplace(root,oldKey,newKey):
    if oldKey == newKey or len(newKey)==0:
        return
    for dname, dirs, files in os.walk(root,topdown=False):
        for filename in files:
            oldfile = join(dname,filename)
            if isfile(oldfile):
                if oldKey in filename:
                    newfile = join(dname,filename.replace(oldKey,newKey))
                    print(oldfile,newfile)
                    os.rename(oldfile,newfile)

        # rename folder 
        if oldKey in basename(dname):
            destfolder = join(Path(dname).parent,basename(dname).replace(oldKey,newKey))
            os.rename(dname,destfolder)

def writing():
    pass
        # rename file
        # replace filecontent
        # for fname in files:
            # fpath = os.path.join(dname, fname)
            # with open(fpath) as f:
                # s = f.read()
            # s = s.replace("${replace}", replacement)
            # with open(fpath, "w+") as f:
                # f.write(s)

def main(args):
    fullReplace(args.root,args.oldKey,args.newKey)

def entry_point():
    parser = createParse()
    mainArgs=parser.parse_args()
    main(mainArgs)

def createParse():
    parser = argparse.ArgumentParser( formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="")
    # subparsers = parser.add_subparsers()
    # eat_parser = subparsers.add_parser('eat',formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="",  help='sub command demo')
    parser.add_argument('-r', '--root',type=str,required=False, help='root', default="")  
    parser.add_argument('-o', '--oldKey',type=str,required=False, help='oldKey', default="")  
    parser.add_argument('-n', '--newKey',type=str,required=False, help='newKey', default="")  
    parser.add_argument('-t', '--test', help='test questions', default=False, action='store_true') 
    return parser
