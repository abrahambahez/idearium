# (sn) git-subtree
Fuente: <https://gist.github.com/SKempin/b7857a6ff6bddb05717cc17a44091202>

```
git subtree add --prefix {local directory being pulled into} {remote repo URL} {remote branch} --squash
```

Explicación:

1. Specify you want to add a subtree
2. Specify the prefix local directory into which you want to pull the subtree
3. Specify the remote repository URL [*of the subtree being pulled in*]
4. Specify the remote branch [*of the subtree being pulled in*]
5. Specify you want to squash all the remote repository's [*the subtree's*] logs

## Pull

La misma fórmula que arriba sustituyendo `add` por `pull`

## Push
La misma fórmula que arriba sustituyendo `add` por `push` y eliminando `--squash`
