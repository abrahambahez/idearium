# RAG
En el contexto de los [[LLM]] y [[procesamiento de lenguaje natural]], el *Retrieval Augmented Generation* (generación aumentada, o mejorada, con recuperación) es una técnica que dota al modelo de contexto suficiente para responder adecuadamente a un [[prompt]].

John Allard [@allard&jarvis2023, min. 0:11:05] propone una [[analogía]]: el RAG es como añadir información a la [[memoria de trabajo]], con el fin de resolver un problema específico. En contraste, el [[ajuste fino]] (entrenamiento orientado a la especialización) es trabajar en la [[memoria a largo plazo]].


Técnicas donde se implementa son:

- [[búsqueda semántica]]
- busqueda categórica (filtro por una categoría como «sentimiento»)
- *agregattion pipeline* (filtro de un *aggregate* o consulta)
- *per user retrieval*, entre muchos otros
