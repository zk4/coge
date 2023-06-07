> How I reuse a existing project as a template effectively? 

![image-20210312140113821](https://raw.githubusercontent.com/zk4/image_backup/main/img/image-20210312140113821.png)

Simple yet powerful code generator.
Make use of existing tool as possiable as we can.

**Small features:**
1. template is runable as normal prj. No more %placehold% stuff.
3. respect .gitignore.
3. support github.com repo.
5. plugin in any language only if you can run it in shell.
7. respect Old keyword case. 

# install
```
pip3 install coge
```

# usage
put this line in your `~/.bash_profile`, and change the `your_template_folder` to  the folder where you put your templates.
```
export COGE_TMPLS="<your_template_folder>"
```

## demo 1
``` bash
coge js react oldkey:newkey :newkey0 :newkey1 @:destname 

# What coge does:
# - copy $COGE_TMPLS/js/react to $PWD/destname
# - change all names from oldkey to newkey,  from  COGE_ARG_0 to newkey0 ,from  COGE_ARG_1 to newkey1

```
## demo 2
``` bash
coge js react
# What coge does:
# - Just copy $COGE_TMPLS/js/react to $PWD/app
```


# advanced tricks (optional)

## work with fzf
``` 
cg () {
	eval `coge -c $@ | fzf --preview= --bind 'enter:execute-silent(pbcopy <<< {})+abort' ` && pbpaste
}
```
call cg from terminal. and paste it.
## hook script
you can put .coge.after.sh in you template folder. 

It will execute after copy, which is very handy.

For Safety reason. Template from network would need to use -s option to enforcing script executing, only if you know the script is safe.

Supported timing and language:
```
.coge.after.sh
.coge.before.sh

.coge.after.py
.coge.before.py
```

Ex:
put .coge.after.sh in your source template
```
#!/bin/bash
echo "init your git repo"
git init 
```

## .coge.json 
Sometimes we do not remember what the string we should repalce,
put a `.coge.json` in your template project.
coge would respect this json file to verify all replacements. 
It is just a array with two types, map or string.
all elements in the array must be fullfilled when doing the replacements.
If some strings to be replaced are missed in the command line. Coge would automatically prompt up for user to supply.

I think the configuration explains for itself.
``` json
[
  {
   "key": "cli",
   "desc": "this is blala"
  },
  "projectname"
]
```


# help
```
usage: coge [-h] [-a ARG_PREFIX] [-l] [-c] [-r] [-R] [-s] [-d DEPTH] [-v]
            [magic ...]

       make template link : cd x-engine-module-template && coge -r 
             use template : coge x-engine-module-template xxxx:camera @:x-engine-module-camera  
use git template from net : coge https://www.github.com/vitejs/vite \bvite\b:your_vite @:your_vite  
    

positional arguments:
  magic                 newkey:oldkey or @:folder_name

optional arguments:
  -h, --help            show this help message and exit
  -a ARG_PREFIX, --arg_prefix ARG_PREFIX
                        ex: COGE_ARG_
  -l, --list            list folders
  -c, --cmd             cmd
  -r, --link_tplt       link `cwd` to $COGE_TMPLS
  -R, --unlink_tplt     unlink `cwd`
  -s, --script_from_net
                        alllow script from net
  -d DEPTH, --depth DEPTH
                        list depth
  -v, --version         version
```
