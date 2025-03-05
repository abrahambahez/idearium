# RAG

En el contexto de los [LLM](LLM.md) y [procesamiento-de-lenguaje-natural](procesamiento-de-lenguaje-natural.md), el *Retrieval Augmented Generation* (generación aumentada, o mejorada, con recuperación) es una técnica que dota al modelo de contexto suficiente para responder adecuadamente a un [prompt](prompt.md).

John Allard [@allard&jarvis2023, min. 0:11:05] propone una [analogia](analogia.md): el RAG es como añadir información a la [memoria-de-trabajo](memoria-de-trabajo.md), con el fin de resolver un problema específico. En contraste, el [ajuste-fino](ajuste-fino.md) (entrenamiento orientado a la especialización) es trabajar en la [memoria-a-largo-plazo](memoria-a-largo-plazo.md).

Técnicas donde se implementa son:

* [busqueda-semantica](busqueda-semantica.md)
* busqueda categórica (filtro por una categoría como «sentimiento»)
* *agregattion pipeline* (filtro de un *aggregate* o consulta)
* *per user retrieval*, entre muchos otros
