#coding: utf-8
from .logx import setup_logging
from .binaryornot import is_binary

# don`t remove this line
import logging
setup_logging()
logger = logging.getLogger(__name__)

import argparse
import os
from os.path import join, isfile,basename
from pathlib import Path
from distutils.dir_util import copy_tree
import re
import subprocess
import shutil

COGE_CONFIG_FILE = ".coge.json"
COGE_HISTORY_FILE = ".coge.history"

common_ignore=[".DS_Store",'.pyc',".o",".obj",".class","Pods"]

def is_git_folder(src):
    try:
        subprocess.check_output(f"cd {src}  && git status ", shell=True).splitlines()
    except Exception as e:
        return False
    return True

# this command will respect .gitignore
def is_git_folder_clean(src):
    list_of_files =[]
    try:
        list_of_files = subprocess.check_output(f"cd {src}  && git status -s", shell=True).splitlines()
    except Exception as e:
        pass
    return len(list_of_files) == 0

def git_ls_files(src):
    before_script=join(src,".coge.before.py")
    list_of_files = subprocess.check_output(f"cd {src}  && git ls-files", shell=True).splitlines()
    return list_of_files

def before_copy(src,dest):
    before_py_script=join(src,".coge.before.py")
    if os.path.isfile(before_py_script):
        logger.warning(f'----------------.coge.before.py----------------------')
        subprocess.Popen(["python3",before_py_script],cwd=dest).communicate()
        logger.warning(f'-----------------------------------------------------')

    before_sh_script=join(src,".coge.before.sh")
    if os.path.isfile(before_sh_script):
        logger.warning(f'----------------.coge.before.sh----------------------')
        subprocess.Popen(["bash" ,before_sh_script],cwd=dest).communicate()
        logger.warning(f'-----------------------------------------------------')

def after_copy(src,dest):
    after_py_script=join(src,".coge.after.py")
    if os.path.isfile(after_py_script):
        logger.warning(f'----------------.coge.after.py----------------------')
        subprocess.Popen(["python3",after_py_script],cwd=dest).communicate()
        logger.warning(f'-----------------------------------------------------')

    after_sh_script=join(src,".coge.after.sh")
    if os.path.isfile(after_sh_script):
        logger.warning(f'----------------.coge.after.sh----------------------')
        subprocess.Popen(["bash" ,after_sh_script],cwd=dest).communicate()
        logger.warning(f'-----------------------------------------------------')

def copying(src,dest):
    if is_git_folder(src):
        #  if not allow_git_dirty and not is_git_folder_clean(src):
        logger.critical(f"if {src} is not clean, commit your changes or git reset. or it will ignore the file changes")
        #      sys.exit(0);


        gitfiles = git_ls_files(src)

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

            try:
                shutil.copy(join(src,f), join(dest,f),follow_symlinks=False)
                logger.info("coge --> "+join(dest,f))
            except Exception as e:
                logger.error("coge --> "+join(dest,f))
                pass
    else:
        logger.critical("Not a git repo,full copy!")
        copy_tree(src, dest)
        logger.warning(f'copy done -------------------------------------------')


def replace_with_case(content,before,after):
    regex = re.compile(re.escape(before), re.I)
    partial= regex.sub(lambda x: ''.join(d.upper() if c.isupper() else d.lower()
        for c,d in zip(x.group()+after[len(x.group()):], after)), content)
    return partial

def full_repalcement(root,oldKey,newKey):
    if oldKey == newKey or len(newKey)==0:
        return

    for dname, dirs, files in os.walk(root,topdown=False):
        dirs[:] = [d for d in dirs if not d == '.git']
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
            if is_binary(oldfile):
                logger.info(oldfile + " is binary!")
                continue

            contents = ""
            try:
                contents = str(Path(oldfile).read_text())
            except Exception as e:
                print(f"{oldfile} error: pass", e)
                continue

            contents = replace_with_case(contents,oldKey,newKey)
            with open(oldfile,"w") as f:
                f.write(contents)

            if isfile(oldfile):
                if oldKey.upper() in filename.upper():
                    newfile = join(dname,replace_with_case(filename,oldKey,newKey))
                    os.rename(oldfile,newfile)

        #  rename folder
        if oldKey.lower() in basename(dname).lower() and (dname != root):
            destfolder = join(Path(dname).parent,replace_with_case(basename(dname),oldKey,newKey))
            os.rename(dname,destfolder)

def get_coge_config(root):
    # Check if the file exists
    target = join(root,COGE_CONFIG_FILE)
    if os.path.isfile(target):
        print("The file exists.")
        import json
        with open(target) as file:
            # Load the contents of the file
            data = json.load(file)
            return data
    else:
        return []

def main(root,args):
    keypairs={}
    prefix = args.arg_prefix or "COGE_ARG_"

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
            keypairs[key] = val

    coge_config =  get_coge_config(root)
    for o in coge_config:
        key  = o
        desc = ""
        if type(o) == dict:
            key = o["key"]
            desc = o["desc"]
        if key not in keypairs:
            if type(key) == str:
                v = input(f'Need key [{key}]: ')
                keypairs[key] = v
            else:
                v = input(f'Need key [{key}], {desc}: ')
                keypairs[key] = v

    
    
    if args.cmd or len(args.magic)==0:
        list_commands(root,args.depth)
        return 

    if args.list or len(args.magic)==0:
        list_target(root,args.depth)
        return 

    cwd = os.getcwd()
    dest = join(cwd,target_foldername)
    if os.path.isdir(dest):
        logger.critical(f"{dest} exists. rm it first!")
        return 

    tempalte_name = args.magic[0]
    is_from_net=tempalte_name.startswith("http://") or tempalte_name.startswith("https://") or tempalte_name.startswith("file://") or tempalte_name.startswith("git@")


    if is_from_net and args.script_from_net:
        logger.critical(f"template is from net! Script will run cause you use -s option! BE CAUTION!")
    if not is_from_net or args.script_from_net:
        before_copy(root,dest)
    else:
        logger.warn(f'before script will not run')

    if is_from_net:
        # -b opencv-2.4 --single-branch
        subprocess.Popen(["git","clone","--depth=1","-b",args.branch, "--single-branch",tempalte_name,dest]).communicate()
    else:
        copying(root,dest)

    for key, val in keypairs.items(): 
        full_repalcement(dest,key,val)

    if not is_from_net or args.script_from_net:
        after_copy(root,dest)
    else:
        logger.warn(f'after script will not run')



def list_target(root,depth):
    stuff = os.path.abspath(os.path.expanduser(os.path.expandvars(root)))

    for dname,dirs,files in os.walk(stuff, followlinks=True):
        dirs[:] = [d for d in dirs if not d == '.git']
        cdepth = dname[len(stuff):].count(os.sep)
        if basename(dname).startswith(".") or ".git" in dname or "__pycache__" in dname:
            continue
        if  cdepth < depth:
            print("     "*(cdepth-1) , basename(dname))

def list_commands(root,depth):
    stuff = os.path.abspath(os.path.expanduser(os.path.expandvars(root)))
    
    for dname,dirs,files in os.walk(stuff, followlinks=True):
        dirs[:] = [d for d in dirs if not d == '.git']
        cdepth = dname[len(stuff):].count(os.sep)
        if basename(dname).startswith(".") or ".git" in dname or "__pycache__" in dname:
            continue
        if  cdepth < depth:
            print("coge",re.sub("/"," ",re.sub(root,"",dname)),"@:app")
        olddepth = cdepth 



def get_root():
    env_root = os.environ.get("COGE_TMPLS") or os.environ.get("CG_TMPLS")
    root  = env_root or os.path.expanduser("~/.config/.code_template")
    return env_root,root

def entry_point():
    parser = create_parser()
    mainArgs=parser.parse_args()
    env_root,root = get_root()
    if(mainArgs.version):
        import pkg_resources  # part of setuptools
        version = pkg_resources.require("coge")[0].version
        print(version)
        return 
    if env_root is None:
        fallbackdir= os.path.expanduser("~/.config/.code_template")
        Path(fallbackdir).mkdir(parents=True, exist_ok=True)
        logger.warning(f"env COGE_TMPLS is not definded! use default tmplts location: {fallbackdir}")

    
    if mainArgs.link_tplt:
        link()
        return 

    if mainArgs.unlink_tplt:
        unlink()
        return 

    main(root,mainArgs)

def link():
    _ ,root = get_root()
    cwd = os.getcwd()
    dest_name = basename(cwd)
    dest_tmpl = f"{root}/{dest_name}"
    if not os.path.isdir(dest_tmpl):
        subprocess.check_output(f"ln  -s $PWD {root}", shell=True)
        logger.info(f'link:{cwd} --> {root}/{dest_name}')
    else:
        logger.warning(f"template {dest_tmpl} exits! Just use it. if you want to unlink it, use coge -R in your source folder")

def unlink():
    _ ,root = get_root()
    cwd = os.getcwd()
    dest_name = basename(cwd)
    dest_tmpl = f"{root}/{dest_name}"
    if os.path.isdir(dest_tmpl):
        subprocess.check_output(f"rm -f  {dest_tmpl}", shell=True)
        logger.info(f'unlink:{cwd} -x- {root}/{dest_name}')
    else:
        logger.warning(f"template {dest_tmpl} dose not exits!")

def create_parser():
    parser = argparse.ArgumentParser( formatter_class=argparse.RawTextHelpFormatter, description="""
       make template link : cd x-engine-module-template && coge -r 
             use template : coge x-engine-module-template xxxx:camera @:x-engine-module-camera  
use git template from net : coge https://www.github.com/vitejs/vite \\bvite\\b:your_vite @:your_vite  
    """)

    parser.add_argument('-b', '--branch',type=str,required=False, help='branch', default="master")  
    parser.add_argument('-a', '--arg_prefix',type=str,required=False, help='ex: COGE_ARG_', default="COGE_ARG_")  
    parser.add_argument('-l', '--list', help='list folders', default=False, action='store_true' ,) 
    parser.add_argument('-c', '--cmd', help='cmd', default=False, action='store_true' ,) 
    parser.add_argument('-r', '--link_tplt', help='link `cwd` to $COGE_TMPLS', default=False, action='store_true' ) 
    parser.add_argument('-R', '--unlink_tplt', help='unlink `cwd`', default=False, action='store_true' ) 
    parser.add_argument('-s', '--script_from_net', help='alllow script from net', default=False, action='store_true' ) 
    parser.add_argument('-d', '--depth',type=int,required=False, help='list depth', default=3)  
    parser.add_argument('-v', '--version', help='version', default=False, action='store_true' ) 
    parser.add_argument('magic', metavar="magic", type=str, nargs='*', 
            help='newkey:oldkey or @:folder_name')
    return parser
