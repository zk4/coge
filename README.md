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
3. respect .gitignore.
4. quick project to template and vice versa.
5. prompt available.

# install
```
make install
```

# API design 
which one you prefer?
```
# no slash
cg js react oldkey:newkey :newkey2 @:destname 

# with slash
cg js/react oldkey:newkey :newkey2 @:destname 
```

# Scenario
## 1
``` bash
cg js react oldkey:newkey :newkey0 :newkey1 @:destname 
```
- copy $CG_TMPLS/js/react to $PWD/destname
- change all names from oldkey to newkey,  from  CG_ARG__0 to newkey0 ,from  CG_ARG__1 to newkey1

## 2
``` bash
cg js react
```
- Just copy $CG_TMPLS/js/react to $PWD/app



