# cg

Compare to hygen, yo. What I need

1. template runable. 
2. respect .gitignore.
3. no more $ placehold. Just wired name holder, I need it compilable.
4. instinct command follow the folder path.
5. quick project to template and vice versa.
6. prompt and args.
7. old template project is updatable from updated template.




# API Design
``` bash
cg js/react -o hello_world 
```

inner process:
- find  $CG_TEMPLATE_FODLER/js/react/ 
- replace `CG_PLACE_HOLDER` with `hello_world` of filename or content, what is `CG_PLACE_HOLDER`? what ever you defined as long as it won't conflict with normal string. like ARGS__haha
- copy $CG_TEMPLATE_FODLER/js/react/  to current folder named hello_world


