# el problema de la reutilización de la misma pieza de información
## Distintas descripciones del problema

En un [[sistema de notas interconectadas]] se suele seguir un [[patrón de retroalimentación corta-larga]] y eso lleva al problema de la reutilización de la misma información en diferentes medios o soportes.

### Roam Research: redundancia y trabajo extra

De acuerdo con [[@white-sullivan2018]] [§3 'Problems with the file cabinet approach', párr. 2], se lee:

>Unlike the brain, the file cabinet approach makes it difficult or impossible to remix or reuse the same piece of information. Each time a change is made to any given file, it has to be tracked down and updated in every location in which it exists. This leads to redundancy, with a cluttering of near-identical ideas, and significant work any time a system-wide change is required.

Esta problemática es resuelto por Roam Reseach a través de las páginas o bloques (párrafos o listas hijas) embebidos, funcionalidad que se conoce como [[transclusión]] (*transclusion*).

### Trilium

En [*Patterns of personal Knowledge base*](https://github.com/zadam/trilium/wiki/Patterns-of-personal-knowledge-base) de la aplicación Trilium, se lee:

>While organizing the notes into the hierarchy, you very quickly run into a dilemma - your note seem to belong to two places in the hierarchy equally. As an example - you want to make a note about [bash](https://en.wikipedia.org/wiki/Bash_(Unix_shell)) - does it belong to "OS / Linux" or "Programming / Scripting languages"? This is actually a false dichotomy forced down by the limits of the basic tree hierarchy - the answer is _of course it belongs to both_. This is the reason why Trilium doesn't use standard tree structure (which requires every note to have exactly one parent), but an extension which allows every note to have several parents, thus effectively allowing it to appear in multiple places in the hierarchy. For lack of better term I call this "[cloning](https://github.com/zadam/trilium/wiki/Cloning-notes)". The main problem with this term is that it suggests that each clone must have an original, but here all clones are completely equal - effectively there's no original.
>In tech lingo, it might be better to describe it as a [hard link](https://en.wikipedia.org/wiki/Hard_link) with an important difference that it is possible to hard link (clone) a directory (inner note).

Trilium lo resuelve a través de lo que llama [«clones»](https://github.com/zadam/trilium/wiki/Cloning-notes), que considera una especie de *hard linking*.

### Obsidian

Obsidian ha implementado también un sistema de [[transclusión]], pero su visualización no es tan buena

## ¿Para qué queremos transcluir una pieza de información? 
En lugar de transcluir, se podrían simplemente *crear nuevas estructuras argumentales* a partir de la indirección que ofrecen las referencias. 

La transclusión permite esbozar una pieza más cercana a la linealidad de un producto final porque es posible controlar el orden del texto. La referencia exige una reelaboración de esa linealidad a partir de las diferentes ramas que ofrecen las referencias; pero el precio a pagar por eso es la unidireccionalidad del proceso. El texto final diverge libremente y será más costoso volver a las notas que lo orginaron porque se les parecerá cada vez menos.