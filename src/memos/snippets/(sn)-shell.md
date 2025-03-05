# (sn) shell
Mover contenido de un archivo (1) a otro (2) y vaciar el contenido del archivo original: 

```bash
cat file1 >> file2 && echo -n "" > file1
```

Seleccionar una línea aleatoria en un archivo de texto y devolverla en stdout

```bash
rl -c 1 <file>
```
