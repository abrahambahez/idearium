# (sn) vim-mkdnflow-plugin
Hice una modificación sobre el código fuente para modificar la creación de wikilinks.

Localmente, la hice en `~\.vim\plugged\mkdnflow.nvim\lua\mkdnflow\links.lua` en la línea **340**.

La línea original, según el [repo de Github](https://github.com/jakewvincent/mkdnflow.nvim/blob/main/lua/mkdnflow/links.lua), está escrita como sigue:

```lua
338    -- Format the replacement depending on the user's link style preference
339    if link_style == 'wiki' then
340        replacement = {'[['..path_text..'|'..text..']]'}
341    else
```


