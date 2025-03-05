# descenso del gradiente

Un algoritmo que ayuda a reducir el error en [modelo-de-IA-generativa](modelo-de-IA-generativa.md), que se define como la diferencia entre los parámetros (y «reglas») del modelo y los datos empíricos.

Este algoritmo encuentra el mínimo o máximo de una función (ej. valles y crestas en un plano cartesiano), llamada *función objetivo* o *función de coste*. El algoritmo se inicia con valores iniciales de los parámetros del modelo (aleatorios o basados en alguna heurística), luego calcula el gradiente y va actualizando los parámetros iterativamente hasta lograr una convergencia satisfactoria.

El gradiente es un vector que indica la dirección y la magnitud del cambio más pronunciado en la función, y así indica cómo ajustar los parámetros para disminuir el valor de la función.

Una forma común de implementarlo es llamada **descenso del gradiente estocástico** (SGD), que calcula el gradiente y actualiza los parámetros usando sólo un ejemplo de entrenamiento a la vez.
