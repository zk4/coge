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
        if not os.path.isfile(src):
            subprocess.check_output(f"cd {src}  && git status ", shell=True).splitlines()
        else:
            return False
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
    print(src,dest)
    if is_git_folder(src):
        logger.critical(f"if {src} is not clean, commit your changes or git reset. or it will ignore the file changes")
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
        if os.path.isfile(src):
            shutil.copyfile(src,dest)
        else:
            copy_tree(src, dest)
            logger.warning(f'copy done -------------------------------------------')


def replace_with_case(content,before,after):
    regex = re.compile(re.escape(before), re.I)
    partial= regex.sub(lambda x: ''.join(d.upper() if c.isupper() else d.lower()
        for c,d in zip(x.group()+after[len(x.group()):], after)), content)
    return partial

def full_repalcement(code_template_folder,oldKey,newKey):
    if oldKey == newKey or len(newKey)==0:
        return

    for dname, dirs, files in os.walk(code_template_folder,topdown=False):
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
        if oldKey.lower() in basename(dname).lower() and (dname != code_template_folder):
            destfolder = join(Path(dname).parent,replace_with_case(basename(dname),oldKey,newKey))
            os.rename(dname,destfolder)

def get_coge_config(code_template_folder):
    # Check if the file exists
    target = join(code_template_folder,COGE_CONFIG_FILE)
    if os.path.isfile(target):
        print("The file exists.")
        import json
        with open(target) as file:
            # Load the contents of the file
            data = json.load(file)
            return data
    else:
        return []

def main(args):
    code_template_folder = get_code_template_folder()
    targets = code_template_folder
    keypairs={}

    target_name = "app"
    for m in args.magic:
        if "." == m:
            pass
        elif ":" not in m:
            print("m",m)
            targets = join(targets,m)
            if os.path.isfile(targets):
                target_name = m
        else:
            ms = m.split(":")
            key = ms[0]
            val = ms[1]
            if key == val:
                print(f"keypair: {key}:{val} must not be the same!")
                return
            if key=="@":
                target_name=val
                continue
            keypairs[key] = val

    coge_config =  get_coge_config(targets)
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
        list_commands(targets,args.depth)
        return

    if args.list or len(args.magic)==0:
        list_target(targets,args.depth)
        return

    cwd = os.getcwd()
    dest = join(cwd,target_name)
    if os.path.isdir(dest):
        logger.critical(f"{dest} exists. rm it first!")
        return

    tempalte_name = args.magic[0]
    is_from_net=tempalte_name.startswith("http://") or tempalte_name.startswith("https://") or tempalte_name.startswith("file://") or tempalte_name.startswith("git@")


    if is_from_net and args.script_from_net:
        logger.critical(f"template is from net! Script will run cause you use -s option! BE CAUTION!")
    if not is_from_net or args.script_from_net:
        before_copy(code_template_folder,dest)
    else:
        logger.warn(f'before script will not run')

    if is_from_net:
        subprocess.Popen(["git","clone","--depth=1","-b",args.branch, "--single-branch",tempalte_name,dest]).communicate()
    else:
        copying(targets,dest)

    for key, val in keypairs.items():
        full_repalcement(dest,key,val)

    if not is_from_net or args.script_from_net:
        after_copy(targets,dest)
    else:
        logger.warn(f'after script will not run')


def list_target(code_template_folder,depth):
    stuff = os.path.abspath(os.path.expanduser(os.path.expandvars(code_template_folder)))

    for dname,dirs,files in os.walk(stuff, followlinks=True):
        dirs[:] = [d for d in dirs if not d == '.git']
        cdepth = dname[len(stuff):].count(os.sep)
        if basename(dname).startswith(".") or ".git" in dname or "__pycache__" in dname:
            continue
        if  cdepth < depth:
            print("     "*(cdepth-1) , basename(dname))

def list_commands(code_template_folder,depth):
    stuff = os.path.abspath(os.path.expanduser(os.path.expandvars(code_template_folder)))

    for dname,dirs,files in os.walk(stuff, followlinks=True):
        dirs[:] = [d for d in dirs if not d == '.git']
        cdepth = dname[len(stuff):].count(os.sep)
        if basename(dname).startswith(".") or ".git" in dname or "__pycache__" in dname:
            continue
        if  cdepth < depth:
            print("coge",re.sub("/"," ",re.sub(code_template_folder,"",dname)),"@:app")



def get_code_template_folder():
    env_root = os.environ.get("COGE_TMPLS") or os.environ.get("CG_TMPLS")
    if env_root is None:
        fallbackdir= os.path.expanduser("~/.config/.code_template")
        Path(fallbackdir).mkdir(parents=True, exist_ok=True)
        logger.warning(f"env COGE_TMPLS is not definded! use default tmplts location: {fallbackdir}")

    code_template_folder  = env_root or os.path.expanduser("~/.config/.code_template")
    return code_template_folder

def entry_point():
    parser = create_parser()
    mainArgs=parser.parse_args()
    if(mainArgs.version):
        import pkg_resources  # part of setuptools
        version = pkg_resources.require("coge")[0].version
        print(version)
        return

    if mainArgs.link_target:
        t = mainArgs.link_target
        apath = os.path.abspath(t)
        link(apath)
        return

    if mainArgs.unlink_target:
        t = mainArgs.unlink_target
        unlink(t)
        return

    main(mainArgs)

def link(apath):
    code_template_folder = get_code_template_folder()
    print(code_template_folder)
    cwd = os.getcwd()
    dest_name = basename(cwd)
    dest_tmpl = f"{code_template_folder}/{dest_name}"

    if not os.path.exists(dest_tmpl):
        logger.info(f'link:{apath} --> {code_template_folder}/{dest_name}')
    else:
        logger.warning(f"target {dest_tmpl} exits! Just use it. if you want to unlink it, use coge -R in your source folder or file")
        exit()

    if os.path.isfile(apath):
        subprocess.check_output(f"ln  -s {apath} {code_template_folder}", shell=True)
    else:
        subprocess.check_output(f"ln  -s {apath} {code_template_folder}", shell=True)

def unlink(dest_name):
    code_template_folder = get_code_template_folder()
    dest_tmpl = f"{code_template_folder}/{dest_name}"
    print(dest_tmpl)
    if os.path.exists(dest_tmpl):
        logger.info(f'Removed. {dest_tmpl}')
    else:
        logger.warning(f"target {dest_tmpl} does not exits!")
        exit()
    subprocess.check_output(f"rm -f  {dest_tmpl}", shell=True)

def create_parser():
    parser = argparse.ArgumentParser( formatter_class=argparse.RawTextHelpFormatter, description="""
       make template link : cd x-engine-module-template && coge -r
             use template : coge x-engine-module-template xxxx:camera @:x-engine-module-camera
use git template from net : coge https://www.github.com/vitejs/vite \\bvite\\b:your_vite @:your_vite
    """)

    parser.add_argument('-b', '--branch',type=str,required=False, help='branch', default="master")
    parser.add_argument('-l', '--list', help='list folders', default=False, action='store_true' ,)
    parser.add_argument('-c', '--cmd', help='cmd', default=False, action='store_true' ,)
    parser.add_argument('-r', '--link_target',type=str,required=False, help='link target to $COGE_TMPLS, target must be a relative folder / file', default="")
    parser.add_argument('-R', '--unlink_target',type=str,required=False, help='unlink target to $COGE_TMPLS, target must be a relative folder / file', default="")

    parser.add_argument('-s', '--script_from_net', help='alllow script from net', default=False, action='store_true' )
    parser.add_argument('-d', '--depth',type=int,required=False, help='list depth', default=3)
    parser.add_argument('-v', '--version', help='version', default=False, action='store_true' )

    parser.add_argument('magic', metavar="magic", type=str, nargs='*',
            help='newkey:oldkey or @:folder_name')
    return parser
