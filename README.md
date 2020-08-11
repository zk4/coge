# cg
Simple yet powerful.

Compare to hygen, yo. What I need

1. [x] template is runable as normal prj. No more $placehold$ stuff.
2. [x] instinct command follow the folder path.
3. respect .gitignore.
4. quick project to template and vice versa.
5. prompt and args.
6. old template project is updatable from updated template.




# API Design
``` bash
cg js/react oldkey:newkey :newkey2 @:destname 
```

inner process:
- find  $CG_TEMPLATE_FODLER/js/react/ 
- replace `CG_PLACE_HOLDER` with `hello_world` of filename or content, what is `CG_PLACE_HOLDER`? what ever you defined as long as it won't conflict with normal string. like ARGS__haha
- copy $CG_TEMPLATE_FODLER/js/react/  to current folder named hello_world



