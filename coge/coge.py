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

common_ignore=[".DS_Store",'.pyc',".o",".obj",".class","Pods"]

def isGitFolder(src):
    try:
        subprocess.check_output(f"cd {src}  && git status ", shell=True).splitlines()
    except Exception as e:
        return False
    return True

# this command will respect .gitignore
def isGitFolderClean(src):
    list_of_files =[]
    try:
        list_of_files = subprocess.check_output(f"cd {src}  && git status -s", shell=True).splitlines()
    except Exception as e:
        pass
    return len(list_of_files) == 0

def gitLsFiles(src):
    # todo  you need to commit your files first
    # print("src",f"cd {src}  && git ls-files")
    list_of_files = subprocess.check_output(f"cd {src}  && git ls-files", shell=True).splitlines()
    return list_of_files

def copying(allow_git_dirty, src,dest):
    if isGitFolder(src):
        if not allow_git_dirty and not isGitFolderClean(src):
            logger.critical(f"{src} is not clean, commit your changes or git reset. or use -w to ignore this check")
            sys.exit(0);

        gitfiles = gitLsFiles(src)

        logger.info(f'{src} is git repo')

        if len(gitfiles)==0:
            logger.warning(f'maybe you should commit your chagnes if you use -w, Nothing found with git ls-files in {src}')
        for f in gitfiles:
            try:
                f = f.decode('utf8')
            except Exception as ee:
                logger.exception(ee)
                continue

            dest_fpath = join(dest,f)
            os.makedirs(os.path.dirname(dest_fpath), exist_ok=True)
            isbreak= False
            for ci in common_ignore:
                if f.endswith(ci):
                    isbreak = True
                    break
            if isbreak:
                continue
            shutil.copy(join(src,f), join(dest,f))
            logger.info("coge --> "+join(dest,f))
    else:
        logger.critical("Not a git repo,full copy!")
        copy_tree(src, dest)
    print("copying done -----------------------------------")


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
                print(f"{oldfile} error: pass", e)
                continue

            contents = contents.replace(oldKey,newKey)

            with open(oldfile,"w") as f:
                f.write(contents)

            if isfile(oldfile):
                if oldKey in filename:
                    newfile = join(dname,filename.replace(oldKey,newKey))
                    os.rename(oldfile,newfile)

        # rename folder 
        if oldKey in basename(dname):
            destfolder = join(Path(dname).parent,basename(dname).replace(oldKey,newKey))
            os.rename(dname,destfolder)

def main(root,args):
    keypais={}
    prefix = args.arg_prefix or "COGE_ARG__"

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

    if args.list or len(args.magic)==0:
        listTarget(root,args.depth)
        return 

    cwd = os.getcwd()
    dest = join(cwd,target_foldername)
    if os.path.isdir(dest):
        logger.critical(f"{dest} exists. rm it first!")
        return 
    allow_git_dirty = args.allow_git_dirty
    copying(allow_git_dirty,root,dest)

    for key, val in keypais.items(): 
        fullReplace(dest,key,val)

def listTarget(root,depth):
    stuff = os.path.abspath(os.path.expanduser(os.path.expandvars(root)))

    for dname,dirs,files in os.walk(stuff, followlinks=True):
        cdepth = dname[len(stuff):].count(os.sep)
        if basename(dname).startswith(".") or ".git" in dname or "__pycache__" in dname:
            continue
        if  cdepth < depth:
            print("     "*(cdepth-1) , basename(dname))



def get_root():
    env_root = os.environ.get("COGE_TMPLS") or os.environ.get("CG_TMPLS")
    root  = env_root or os.path.expanduser("~/.config/.code_template")
    return env_root,root

def entry_point():
    parser = createParse()
    mainArgs=parser.parse_args()
    env_root,root = get_root()
    if env_root is None:
        fallbackdir= os.path.expanduser("~/.config/.code_template")
        Path(fallbackdir).mkdir(parents=True, exist_ok=True)
        logger.warning(f"env COGE_TMPLS is not definded! use default tmplts location: {fallbackdir}")

    
    if mainArgs.link_tplt:
        link()
    else:
        main(root,mainArgs)

def link():
    env_root,root = get_root()
    subprocess.check_output(f"ln  -s $PWD {root}", shell=True)

def createParse():
    parser = argparse.ArgumentParser( formatter_class=argparse.RawTextHelpFormatter, description="""
      make template link : cd x-engine-module-template && coge -r 
            use template : coge x-engine-module-template xxxx:camera @:x-engine-module-camera  
    """)

    parser.add_argument('-a', '--arg_prefix',type=str,required=False, help='ex: COGE_ARG__', default="COGE_ARG__")  
    parser.add_argument('-l', '--list', help='list folders', default=False, action='store_true' ,) 
    parser.add_argument('-r', '--link_tplt', help='link `cwd` to $COGE_TMPLS', default=False, action='store_true' ) 
    # parser.add_argument('-i', '--init', help='init your COGE_TMPLS location to ~/.config/.code_template', default=False, action='store_true' ) 
    parser.add_argument('-w', '--allow_git_dirty', help='alllow git dirty', default=False, action='store_true' ) 
    parser.add_argument('-d', '--depth',type=int,required=False, help='list depth', default=3)  
    parser.add_argument('magic', metavar="magic", type=str, nargs='*', 
            help='folder or newkey:oldkey')
    return parser
