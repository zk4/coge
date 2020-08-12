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
from distutils.dir_util import copy_tree
import subprocess
import shutil

common_ignore=[".DS_Store",'.pyc',".o",".obj",".class"]

# this command will respect .gitignore
def gitLsFiles(src):
    list_of_files = subprocess.check_output(f"cd {src}  && git ls-files", shell=True).splitlines()
    return list_of_files

def copying(src,dest):
    # copy_tree(src, dest)
    for f in gitLsFiles(src):
        f = f.decode('utf8')
        dest_fpath = join(dest,f)
        os.makedirs(os.path.dirname(dest_fpath), exist_ok=True)
        isbreak= False
        for ci in common_ignore:
            print(type(f),f,"-->",type(ci),ci)
            if f.endswith(ci):
                isbreak = True
                break
        if isbreak:
            continue
        shutil.copy(join(src,f), join(dest,f))


def fullReplace(root,oldKey,newKey):
    if oldKey == newKey or len(newKey)==0:
        return

    for dname, dirs, files in os.walk(root,topdown=False):
        for filename in files:

            # this is evil file from MAC
            isbreak= False
            for ci in common_ignore:
                if filename.endswith(ci):
                    isbreak = True
                    break

            if isbreak:
                continue

            oldfile = join(dname,filename)

            contents = ""
            try:
                contents = str(Path(oldfile).read_text())
            except Exception as e:
                print("error: pass", e)
                continue


            contents = contents.replace(oldKey,newKey)

            with open(oldfile,"w") as f:
                f.write(contents)

            if isfile(oldfile):
                if oldKey in filename:
                    newfile = join(dname,filename.replace(oldKey,newKey))
                    print(oldfile,newfile)
                    os.rename(oldfile,newfile)

        # rename folder 
        if oldKey in basename(dname):
            destfolder = join(Path(dname).parent,basename(dname).replace(oldKey,newKey))
            os.rename(dname,destfolder)

def main(root,args):
    keypais={}
    prefix = args.arg_prefix or "CG_ARG__"
    print(args.magic)

    idx = 0

    target_foldername = "app"
    for m in args.magic:
        if ":" not in m:
            root = join(root,m)
        else:
            ms = m.split(":")
            key = ms[0]
            val = ms[1]
            if key == val:
                print(f"keypair: {key}:{val} must not be the same!")
                return 
            if key=="@":
                target_foldername=val
                continue
            if len(key.strip()) == 0:
                key = prefix +str(idx)
                idx+=1
            keypais[key] = val
        
    print(root,keypais)

    if args.list:
        listTarget(root,args.depth)
        return 

    cwd = os.getcwd()
    dest = join(cwd,target_foldername)
    copying(root,dest)

    for key, val in keypais.items(): 
        fullReplace(dest,key,val)

def listTarget(root,depth):
    stuff = os.path.abspath(os.path.expanduser(os.path.expandvars(root)))

    for dname,dirs,files in os.walk(stuff):
        cdepth = dname[len(stuff):].count(os.sep)
        if  cdepth < depth:
            print("     "*(cdepth-1) , basename(dname))

def entry_point():
    parser = createParse()
    mainArgs=parser.parse_args()
    root  = os.environ.get("CG_TMPLS")
    if root is None:
        print("env CG_TMPLS is not definded!")
        return

    if mainArgs.link_tplt:
        link()
    else:
        main(root,mainArgs)

def link():
    subprocess.check_output("ln  -s $PWD $CG_TMPLS", shell=True)

def createParse():
    parser = argparse.ArgumentParser( formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="")

    parser.add_argument('magic', metavar="o", type=str, nargs='*',
            help='folder or newkey:oldkey')

    parser.add_argument('-a', '--arg_prefix',type=str,required=False, help='ex: CG_ARG__', default="CG_ARG__")  
    parser.add_argument('-l', '--list', help='list folders', default=False, action='store_true' ,) 
    parser.add_argument('-r', '--link_tplt', help='link cwd template to CG_TMPLS', default=False, action='store_true' ) 
    parser.add_argument('-d', '--depth',type=int,required=False, help='list depth', default=3)  
    return parser
