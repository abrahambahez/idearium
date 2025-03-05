# espacio de oportunidad

Rango de deseos y necesidades que una solución puede cumplir en el proceso de [descubrimiento-continuo-de-producto](descubrimiento-continuo-de-producto.md). Puede considerarse toda el área de oportunidades que aparece en el [arbol-de-oportunidad-solucion](arbol-de-oportunidad-solucion.md).

Para esto se puede usar un [mapa-de-experiencia](mapa-de-experiencia.md) validado con [entrevista-a-cliente](entrevista-a-cliente.md). El mapa ordena las diferentes historias (narrativas) de los usuarios.

Es trabajo del *Product Manager* identificar las más importantes (por impacto) y ordenarlas semánticamente en ramas del árbol, para eso puede usar:

* Un proceso de clusterización o agrupamiento de oportunidades similares
* Un proceso inductivo de [categorizacion](categorizacion.md) basado en los términos del usuario ([emic](emic.md))

La estructura debe ser inductiva, de ser posible, dos oportunidades muy similares deberían tener una oportunidad padre más abstracta:, como en el ejemplo sobre oportunidades de Netflix [@torres2021, 90]:

````mermaid
flowchart TD
A("I want\nto watch shows\non the go") --> B1("I want\nto watch in the plane")
A --> B2("I want\nto watch\non my train commute")
````
