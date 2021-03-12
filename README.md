# coge

Simple yet powerful code generator.
Make use of existing tool as possiable as we can.

Compare to hygen, yo.
- yo is way too slow and complicated.
- hygen pollutes all template files, and only support ejs.

**What I only need:**
1. [x] template is runable as normal prj. No more \$placehold\$ stuff.
2. [x] instinct command with the power of fzf.
4. [x] quick project to template and vice versa.
3. [x] respect .gitignore.
3. [ ] support github.com repo.
5. plugin in any language only if you can run it in shell.

# install
```
make install
```

# usage
```
export COGE_TMPLS="<your_template_folder>"
```

## 1
``` bash
coge js react oldkey:newkey :newkey0 :newkey1 @:destname 
```
What coge does:

- copy $COGE_TMPLS/js/react to $PWD/destname
- change all names from oldkey to newkey,  from  COGE_ARG_0 to newkey0 ,from  COGE_ARG_1 to newkey1

## 2
``` bash
coge js react
```
What coge does:
- Just copy $COGE_TMPLS/js/react to $PWD/app


# work with fzf
``` 
cg () {
	eval `coge -c $@ | fzf --preview= --bind 'enter:execute-silent(pbcopy <<< {})+abort' ` && pbpaste
}
```
call cg from terminal. and paste it.


# timing script 
you can put .coge.after.copy.sh in you template folder. 

It will execute after copy, which is very handy.

For Safety reason. Template from network would need to use -s option to enforcing script executing, only if you know the script is safe.

Supported timing and language:
```
.coge.after.copy.sh
.coge.before.copy.sh

.coge.after.copy.py
.coge.before.copy.py
```

Ex:
.coge.after.copy.sh
```
#!/bin/bash
git init 
git flow init
```


# help
```
usage: coge [-h] [-a ARG_PREFIX] [-l] [-c] [-r] [-w] [-d DEPTH]
            [magic [magic ...]]

       make template link : cd x-engine-module-template && coge -r 
             use template : coge x-engine-module-template xxxx:camera @:x-engine-module-camera  
use git template from net : coge https://www.github.com/zk4/x-engine-module-template xxxx:camera @:x-engine-module-camera  
    

positional arguments:
  magic                 folder or newkey:oldkey

optional arguments:
  -h, --help            show this help message and exit
  -a ARG_PREFIX, --arg_prefix ARG_PREFIX
                        ex: COGE_ARG_
  -l, --list            list folders
  -c, --cmd             cmd
  -r, --link_tplt       link `cwd` to $COGE_TMPLS
  -w, --allow_git_dirty
                        alllow git dirty
  -d DEPTH, --depth DEPTH
                        list depth
``` 
