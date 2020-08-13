# coge

Simple yet powerful code generator.
Make use of your shell as possiable as coge can.

Compare to hygen, yo.
- yo is way too slow and complicated.
- hygen pollutes all template files, and only support ejs.

**What I only need:**
1. [x] template is runable as normal prj. No more \$placehold\$ stuff.
2. [x] instinct command follows the folder path.
4. [x] quick project to template and vice versa.
3. [x] respect .gitignore.
3. [ ] support github.com repo.
4. auto complete in command line.
5. prompt available.

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
- change all names from oldkey to newkey,  from  COGE_ARG__0 to newkey0 ,from  COGE_ARG__1 to newkey1

## 2
``` bash
coge js react
```
What coge does:
- Just copy $COGE_TMPLS/js/react to $PWD/app




# help
```
usage: coge [-h] [-a ARG_PREFIX] [-l] [-r] [-w] [-d DEPTH] [o [o ...]]

positional arguments:
  o                     folder or newkey:oldkey (default: None)

optional arguments:
  -h, --help            show this help message and exit
  -a ARG_PREFIX, --arg_prefix ARG_PREFIX
                        ex: CG_ARG__ (default: COGE_ARG__)
  -l, --list            list folders (default: False)
  -r, --link_tplt       link cwd template to COGE_TMPLS (default: False)
  -w, --allow_git_dirty
                        by default, your COGE_TMPLS must git clean, because coge
                        relies on git command if you are in a git repo
                        (default: False)
  -d DEPTH, --depth DEPTH
                        list depth (default: 3)

``` 
