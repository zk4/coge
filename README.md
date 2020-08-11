# cg

Simple yet powerful code generator.
Make use of your shell as possiable as cg can.

Pity, the name cg is taken by others. use `cgr` in cmdline. maybe you should `alias cg=cgr`

Compare to hygen, yo.
- yo is way too slow and complicated.
- hygen pollutes all template files, and only support ejs.

**What I only need:**
1. [x] template is runable as normal prj. No more \$placehold\$ stuff.
2. [x] instinct command follows the folder path.
4. [x] quick project to template and vice versa.
3. respect .gitignore.
5. prompt available.

# install
```
make install
```

# usage
```
export CG_TMPLS="<your_template_folder>"
```

## 1
``` bash
cgr js react oldkey:newkey :newkey0 :newkey1 @:destname 
```
What cg does:

- copy $CG_TMPLS/js/react to $PWD/destname
- change all names from oldkey to newkey,  from  CG_ARG__0 to newkey0 ,from  CG_ARG__1 to newkey1

## 2
``` bash
cg js react
```
What cg does:
- Just copy $CG_TMPLS/js/react to $PWD/app




# help
```
usage: cg [-h] [-a ARG_PREFIX] [-l] [-d DEPTH] [o [o ...]]

positional arguments:
  o                     folder or newkey:oldkey (default: None)

optional arguments:
  -h, --help            show this help message and exit
  -a ARG_PREFIX, --arg_prefix ARG_PREFIX
                        ex: CG_ARG__ (default: CG_ARG__)
  -l, --list            list folders (default: False)
  -d DEPTH, --depth DEPTH
                        list depth (default: 3)


``` 
