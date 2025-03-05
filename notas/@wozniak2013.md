# Incremental learning (SuperMemo 16)

Piotr A Wozniak (2013)

Aprendizaje incremental es el nombre que Wozniak le da al conjunto de técnicas que explotan el uso de algoritmos de [repeticion-espaciada](repeticion-espaciada.md) para la resolución de problemas cognitivos a largo plazo ([tecnica-de-aprendizaje](tecnica-de-aprendizaje.md)).

El proceso tiene una forma similar al [modelo-captura-proceso-ejecucion-retroalimentacion](modelo-captura-proceso-ejecucion-retroalimentacion.md), pues lo describe como:

````mermaid
graph TD

A(importing knowledge) <--> B(Prioritizing)
B <--> C(Learning materials ><br/>Lasting Knowledge)
C <--> D(Expanding creatively)
````

Textualmente [@wozniak2013, § 'General outline of incremental learning'] afirma que:

 >
 > * Importar conocimiento de diversas fuentes electrónicas y no electrónicas (por ejemplo, artículos en la web, videos de YouTube, archivos de música, imágenes de tu cámara, correos electrónicos, notas escaneadas en papel, etc.).
 > * Priorizar el conocimiento para su procesamiento incremental (por ejemplo, alta prioridad para la física, baja prioridad para datos curiosos de películas, etc.). El enfoque incremental implica procesar el conocimiento en pequeños fragmentos y en pequeños pasos.
 > * Convertir gradualmente los materiales de aprendizaje en conocimiento duradero en tu memoria. Esta conversión también puede generar un archivo de medios informáticos fácilmente buscable y bien anotado que ni siquiera necesita ser parte del proceso de aprendizaje.
 > * Expandirse creativamente sobre el conocimiento adquirido (por ejemplo, en el proceso de escritura incremental, resolución de problemas, etc.).

Principios formales básicos

* Interrupción o *Interleaving* [§ 'The value of interruption in learning']

Aplicaciones:

* La [lectura-incremental](lectura-incremental.md) es la base más consolidada de su programa, reconoce dos unidades: *topics* (textos por leer, esperan extracción de información de valor) e *items* (material de repaso, prueba el conocimiento)
  * En supermemo es posible leer subconjuntos temáticos (si son parte de un examen)
