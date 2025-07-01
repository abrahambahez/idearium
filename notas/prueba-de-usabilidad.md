# prueba de usabilidad
Siguiendo propuestas elaboradas por Norman Nielsen Group, una consultora especializada en pruebas de [[usabilidad]], estas pruebas pueden dividirse en dos clases [@budiu2017] con objetivos diversos pero complementarios:

1. Pruebas de usabilidad cualitativas. Su objetivo es encontrar problemas de usabilidad en prototipos de la forma más rápida posible a través de pruebas a pocas personas (cinco se considera un número ideal para encontrar la mayoría de problemas de usabilidad), se orienta a entender *por qué* las personas usan una interfaz del modo en que lo hacen
2. Pruebas de usabilidad cuantitativas. Su objetivo es probar la generalidad del producto a partir de una muestra más variada y representativa de personas, identificando elementos cuantificables como: tasas de éxito para completar tareas determinadas, tasas de rebote (tiempo que tarda un usuario en salir de la plataforma tras haber entrado), es capaz de medir la usabilidad general de una funcionalidad.

A continuación se elabora una ficha metodológica breve con las pautas principales.

Pruebas de usabilidad basadas en casos de uso o historias de usuario y matriz de observación.

Definiciones iniciales:

1. Caso de uso: Los casos de uso son formas de especificar interacciones de un usuario sobre un sistema orientadas a un resultado particular. Estas especificaciones usan el lenguaje natural para describir de forma convencional las tareas, si todas las descripciones son simples [y orientadas a metas, @krug2010] y siguen los mismos patrones, las pruebas pueden extender su validez [@phalp&al2007]. Algunos modelos sencillos son:
    1. Sujeto-verbo-objeto: La investigadora busca información
    2. Sujeto-verbo-complemento: El servidor público intenta reconocer en dónde encontrar información para subir información
2. Historia de usuario: Las historias de usuario son casos de uso más contextualizados tanto en la dimensión del usuario como en la de la meta. Utilizan modelos predefinidos que permiten estandarizar su evaluación y contribuyen a comunicar el valor del caso de uso entre diversas partes interesadas [@lucassenetal2016]. El modelo más usado es el siguiente:
    1. Como un(a) \[usuario(a)\], quiero \[meta accionable\] para poder lograr \[resultado o beneficio\]
    2. Ejemplo: como activista en derechos del agua, quiero descargar información entendible y confiable que no venga de fuentes gubernamentales para poder usarla como evidencia jurídica
3. Matriz de observación: La matriz de observación es una herramienta que *operacionaliza* [@reguantalvarez&martinezolmo2014] elementos observables en una situación de campo, estos elementos se escogen por su pertinencia como unidades de análisis o su importancia complementaria para entender un objetivo de investigación más grande. En este caso, el instrumento sirve al propósito de obtener más información contextual sobre la *situación de interacción* persona-aplicación

Pasos de implementación

4. Definir caso de uso o historia de usuario a probar (ver plantillas propuestas)
5. Definir matriz de observación con variables relevantes. Para hacer una análisis comparativo relevante sería recomendable que, aunque el caso de uso pueda variar, las variables a observar se mantengan iguales en todas las pruebas. La recomendación es usar tres categorías generales: actividades (descripción precisa de qué hace el usuario, poniendo atención a cuáles son los pasos que sigue), expresiones (citas textuales de expresiones verbales que pueden ir acompañadas de descripciones contextuales), indicadores emocionales (descripciones de expresiones corporales o tonos de voz que reflejen estados de ánimo como sorpresa, frustración, )
6. Escribir un guion de trabajo: El guion de trabajo incluye la presentación del ejercicio y la descripción de las dinámicas, así como documenta el paso a paso ideal que la plataforma ofrece para resolver el caso de uso o historia de usuario
7. Implementar el guion en taller. Proceso de implementación en campo
8. Analizar resultados. Este momento puede hacerse en combinación con otros datos obtenidos de metodologías complementarias o sobre los datos de la prueba. El análisis inicial sería la colección descriptiva de los diversos pasos realmente ejecutados, que debería compararse con los pasos que provee la plataforma para identificar diferencias y profundizar en las causas. También la identificación de *"puntos de dolor"* o momentos importantes de emociones negativas de los usuarios, enfatizando el rol que la interfaz tuvo en detonar, agravar o minimizar el estado de ánimo

Herramientas:

- Plantillas de caso de uso (ver definición)
- Plantillas de historia de usuario (se recomienda )
- Matriz de observación propuesta
- Plantilla de guion de trabajo (se define a coninuación)

Ejemplo de una plantilla de guion de trabajo:


**Requisitos**

- Personas requeridas
    - Tomador de notas (definir cuántas personas, de preferencia un número similar al de personas que probarán simultáneamente)
    - Facilitador(a)
    - Usuarios (definir cuántos)
- Prototipo visual o liga a la plataforma (con internet, etc)
- Preparar la hoja de observación 
- Caso de uso o historia de usuario visible o impresa
- Sala virtual (o presencial)

**Historia de uso a probar**

Como investigadora, quiero encontrar un dato en la plataforma que sé que ya existe y del cual conozco al menos un elemento textual del título, descripción o fuente para poder verlo en la plataforma de la forma más rápida y simple posible

**Pasos proporcionados por la plataforma**

1. Usuario comienza en el Home
2. Usuario da click en ícono de lupa para acceder a la búsqueda global
3. Usuario escribe el término de búsqueda y doy enter
4. Usuario lo que buscaba ya sea gráfica o documento
5. Usuario hace click en el elemento para acceder a la vista original en Home o biblioteca

**Script facilitador**

- Presentación
    - Saludos y presentación
    - Recordar quiénes somos
    - Qué vamos a hacer
        - El propósito de la sesión es explorar junto contigo una nueva funcionalidad para encontrar elementos en la plataforma de los cuales ubicamos nombre o título. Para eso te vamos a dar un objetivo de uso de la aplicación, te guiaremos en los pasos para cumplir ese objetivo y al final comentaremos qué tan útil te fue y qué tanto te ayudaría a resolver tus necesidades de análisis en redes sociales.
        - Vamos a trabajar con un prototipo, esto es, una versión dummy de cómo sería el producto final. Ni los datos ni las descripciones en este diseño son necesariamente reales o significan algo en la realidad
        - Nos gustaría poder grabar esta sesión si estás de acuerdo para fines de evaluación internos. Únicamente KarmaPulse tendrá acceso a tus datos, y bajo ningún concepto, estos serán cedidos, compartidos, transferidos, ni vendidos a ningún tercero.       
- Facilitador manda al usuario el link del prototipo/producto
- Facilitador le *envía por chat el objetivo escrito* (o se lo da impreso) al usuario para que lo lea en voz alta antes de comenzar.
- Facilitador guía la sesión
    - El facilitador no explica la plataforma, si el usuario tiene dudas, el facilitador responde con cosas como ¿tú dónde esperarías que se encuentre el botón que buscas? ¿qué esperas que suceda si haces click en ese botón? ¿cómo interpretas el texto que aparece en esta parte de la interfaz?
- **Sesión de plática abierta**
    - ¿Crees que lograste el objetivo?
    - ¿Qué faltó para lograr el objetivo?
    - ¿Qué salió bien para lograr el objetivo
    - ¿Tienes alguna duda o comentario final?
- Cierre y despedida
    
**Checklist calidad** (para medir el cumplimiento de la estructura de la sesión)

Antes de la presentación 
- [x] Se tienen a la mano los enlaces, la hoja de evaluación y las personas de Karma 
- [x] Los involucrados leyeron las notas previas sobre el usuario

Al terminar la presentación

- [x] Se siguió el script fielmente
- [x] Se leyó textualmente el mensaje de qué vamos a hacer
- [x] El usuario aclaró todas sus dudas
- [x] Se llenaron todos los campos de la evaluación