# wikis semánticas como propuesta al problema de representación del conocimiento
Las Wikis semánticas en muchos casos pueden contener un marco lógico aunque no implique un esquema de clasificación, de modo que podemos tener `isSubclassOf`  pero ninguna subclase [@altheim2008, sect. semantic wikis, párr. 2]

Altheim cita algunos problemas semánticos [@altheim2008, sect. semantic wikis, párr. 3]:

- **ambiguedad lingüística / gramatical**: *homografía* (identidad ortográfica con diferente significado), *polisemia* (diferentes acepciones para el mismo término), *sinónimos no conectados* (referencias al mismo significado que no están relacionadas)
- **falta de contexto**: usos temporales, espaciales, culturales e individuales del lenguaje
- términos no definidos o mal escritos
- identidad ambigua o no definida de materias / temas
- el uso de términos *a priori* basados en el [razonamiento monótono](https://www.jstor.org/stable/23915338?seq=1), entre otros

Muchos, tal vez la mayoría de estos problemas son insuperables **a menos que se force a los usuarios a entender y seguir reglas proscriptivas** [@altheim2008, sect. semantic wikis, párr. 3]

## un marco de aserción estilo wiki según @altheim2008

- La [aserción en sentido informático](https://es.wikipedia.org/wiki/Aserci%C3%B3n_(inform%C3%A1tica)) es un predicado (evaluable como falso o verdadero) sobre el cual se pueden establecer operaciones basadas en estados informacionales.
- La propuesta de Altheim es una librería llamada «AssertionFramework», capaz de categorizar, clasificar y organizar un _corpus_ de documentos a partir de abstracciones que permiten crear aserciones para crear una ontología informal [@altheim2008, sect. Design, párr. 1]

#### clasificación versus ontología

Para @altheim2008:

- We have a readily available solution for an organizational structure that avoids the epistemological conundrums of computer-based ontologies by appealing to the functional (i.e., functionalist) approach of classification systems within library science.
- The terms in a subject language differ referentially from those in ontology or in natural language in that they do not refer to entities or concepts in the real world but to subjects.        
    - ==The extensional meaning of a term in a subject language does not refer to the class of all entities denoted by the term but to the class of documents that the term denotes.==
