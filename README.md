# cg

Compare to hygen, yo. What I need

1. template runable. respect .gitignore, no more $ placehold. Just wired name holders. 
2. instinct command.
3. quick project to template and vice versa.
4. prompt and args ? I don't need that.


And I think. Basic bash command should do the trick. 

# API Design
``` bash
cg js/react -o hello_world 
```

inner process:
- find  $CG_TEMPLATE_FODLER/js/react/ 
- replace `CG_PLACE_HOLDER` with `hello_world` of filename or content, what is `CG_PLACE_HOLDER`? what ever you defined as long as it won't conflict with normal string.
- copy $CG_TEMPLATE_FODLER/js/react/  to current folder named hello_world


