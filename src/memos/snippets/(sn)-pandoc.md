# (sn) pandoc
Exportar a md con citas hechas

```pandoc
pandoc -s --citeproc -t markdown-citations-fenced_divs-native_divs-raw_html  --bibliography=librero.bib -o ~/Documents/dev/sabhz-web/src/pages/optimizar-el-tiempo.md optimizar-el-tiempo.md
```
