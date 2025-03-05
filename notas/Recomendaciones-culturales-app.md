# Recomendaciones culturales app

*Sergio Barrera,* 8 de junio 2024

# Resumen

Este proyecto se centra en desarrollar un sistema de recomendación personalizado para eventos culturales en Mérida, Yucatán. El objetivo es optimizar la relación entre la oferta y la demanda cultural en la ciudad, mejorando la eficiencia de la difusión de eventos y experiencias culturales. El sistema extraerá información de diversas fuentes digitales para crear una base de datos de la oferta cultural disponible. Luego, se recogerán datos mínimos pero esenciales sobre los usuarios para perfilar su demanda cultural. Esto permitirá que el sistema realice recomendaciones basadas tanto en el contenido como en la colaboración de los usuarios, proporcionando sugerencias más relevantes y personalizadas. Además, el modelo de negocio podría basarse en cobrar una comisión por transacción proveniente del sistema o solicitar fondos del presupuesto de difusión de la cartelera cultural de la ciudad. En resumen, este proyecto busca mejorar la experiencia cultural de los habitantes de Mérida y potencialmente impulsar la economía cultural local.

# I. Caso de negocio

## A. Descripción del problema: la relación entre oferta y demanda cultural en Mérida, Yucatán, es ineficiente

La oferta cultural de Mérida.

La ciudad de Mérida posee una creciente oferta cultural que proviene de varios contextos. Existen los eventos culturales y turísticos promovidos por diversos niveles del gobierno; también las iniciativas privadas con fines de lucro (que producen la oferta con la intención de obtener utilidad); las iniciativas privadas sin fines de lucro, como los patronatos o las Fundaciones (que patrocinan la producción de oferta sin la intención de obtener utilidad); la oferta cultural promovida por organizaciones civiles (sin fines de lucro y sin financiamiento privado como único medio), finalmente, la oferta producida por proyectos independientes, alternativos, provenientes de colectivos o iniciativas personales de artistas.

Esta oferta se desarrolla en el contexto de una ciudad donde el turismo es una de las fuentes principales de ingreso. De aquí que exista un interés político y económico en que se mantenga una oferta diversa y creciente. Como consecuencia secundaria, artistas yucatecos, mexicanos y extranjeros también están probando suerte y contribuyendo a la generación de oferta cultural.

Los eventos y productos van desde el ámbito de *lo folklórico* (patrimonio tangible e intangible maya o yucateco, como arqueología, arquitectura, gastronomía, el carnaval y diversas fiestas regionales), a lo *internacional* (galerías, cocinas de autor, librerías especializadas) y lo alternativo (teatro independiente, danza fusión, tocadas «ilegales» en predios privados). Por supuesto, los precios de consumo cultural varían grandemente de lo gratuito a lo millonario.

La demanda cultural en Mérida.

En la ciudad también existe una demanda diversa y variada de consumo cultural, que, teóricamente, tiende a corresponderse con la oferta. La diversidad socioeconómica de la región y su relación con recientes olas de inmigración nacional y extranjera la han vuelto un lugar donde pueden coexistir lenguajes, intereses, niveles de ingreso y valores culturales muy diversos. Aunque la tendencia a recibir población con ingresos medios, altos y muy altos ha ido aumentando. Esto refuerza una tendencia histórica que tiene la ciudad, como otras en la región y el país, a incrementar la desigualdad de ingreso. Lo cual impacta en el acceso al consumo cultural de los habitantes.

Estas características han reforzado una «clase cosmopolita» asentada en la ciudad (particularmente en la zonas del centro histórico y el norte de la ciudad). También el incremento de una demanda de tipo «clase media», mientras que la cultura popular se ha ido replegando a las zonas que están fuera de los circuitos culturales oficiales.

El problema.

La oferta cultural no tiene una difusión eficiente, es decir, las personas que potencialmente consumirían ciertos productos o eventos culturales no llegan a conocerlos todos, sino hasta muy tarde, en muchos casos después de haber sido anunciados. Sus decisiones están limitadas a las que ofrecen sus redes sociales y en el momento en que las comparten con ellos.

Podríamos pensar que una plataforma como Facebook podría resolver esto, puesto que la oferta y la demanda están presentes virtualmente en la plataforma. Pero el problema es que esa plataforma está sobresaturada de otra información, otra oferta y otros intereses de consumo de los usuarios. Esto hace que, aunque *potencialmente* una persona pueda enterarse de todo evento de su interés, es poco probable que, de hecho, se entere de él.

Por otra parte, como es esperable, los recursos y medios de difusión varían mucho, mientras que algunos eventos o tipos de oferta tienen mucho más presupuesto y canales digitales/analógicos de difusión. Otros solo usan redes sociales, canales de WhatsApp y con el mínimo o nulo presupuesto. Pero una plataforma que distribuya la información de la oferta con los perfiles de la demanda más idóneos para consumirla puede volver más efectiva la difusión, así como ayudar a los eventos con menos presupuesto a llegar a personas adecuadas sin incrementar sus costos de difusión.

## B. Descripción del problema en términos de datos

Este es un problema de distribución de información. En términos generales, puede resolverse optimizando la distribución de la información de la oferta cultural hacia las personas potencialmente interesadas. Para eso es necesario tener la mayor cantidad de información posible sobre la oferta y un mínimo de información necesaria de los perfiles de personas que representan la demanda. Luego se podrían implementar diversos modelos de recomendación sensibles a parámetros como intereses, presupuesto de la persona, sus redes sociales, cercanía del evento en el tiempo, entre otros.

En términos de una visión, diría que:

⛰️

Las personas deberían poder tener acceso a la información cultural más relevante para ellos en el mejor momento posible, para que puedan aprovechar al máximo el tiempo que dedican a las actividades culturales, las cuales refuerzan su identidad personal, social y sus vínculos con el lugar donde viven.

# II. Aplicación de la ciencia de datos

## A. Extracción, limpieza y enriquecimiento de los datos sobre la oferta cultural

Los medios digitales son, en principio, los más adecuados para extraer información de la oferta cultural.

No son los únicos, y en algunos casos, no llegan adecuadamente a todas las personas por cuestiones de infraestructura, acceso a recursos como ancho de banda, o condiciones como la literacidad digital de las personas. En este sentido, Facebook es una de las plataformas que más ha invertido en resolver esas limitantes. Por ejemplo, es gratis con planes económicos de la mayoría de los proveedores de telefonía, y tiene versiones funcionales para teléfonos viejos, muchas personas de amplios rangos de edad saben usarlo de forma básica. Esto ha hecho que mucha de la oferta cultural esté publicada allí. Pero como ya comenté, eso no hace óptimo que los usuarios encuentren la oferta cultural *dentro* de la plataforma.

Por lo tanto, la hipótesis de extracción que propongo es la siguiente: Extraer información de las siguientes fuentes es suficiente para tener suficientes datos de la oferta cultural de Mérida:

* Páginas de Facebook de los ofertantes (gobierno, privados que lucran, privados que no lucran, organizaciones civiles, independientes)

* Páginas de agenda cultural del gobierno

* Páginas de agenda cultural de los *lugares privados* (Auditorio de La Isla en Mérida, Foro GNP, algunos bares famosos por presentaciones de artistas)

Esta información tiene una estructura heterogénea, por tanto, lo correcto sería definir un esquema de datos mínimo para estandarizar los campos mínimos con los cuales trabajar.

Por otra parte, sería posible enriquecer esa información con un campo de categorías culturales que nos permita clasificar los tipos de eventos para aumentar la probabilidad de que se filtren correctamente.

## B. Obtención de los datos mínimos necesarios para perfilar la demanda cultural

El perfil personal de las personas es necesario para poder darles una recomendación adecuada. Pero a diferencia de la oferta, donde se pretende obtener la mayor cantidad posible de información, por razones éticas y normativas, es más adecuado obtener la menor cantidad necesaria para ofrecer una buena recomendación.

En principio, mi hipótesis es que esos datos son los siguientes:

* Una forma para llamar a la persona (su nombre, un *user name* o un apodo)

* Una descripción suya sobre cómo se identifica en relación con lo que consume (algo así como la descripción de un perfil de Twitter pero orientado a sus gustos personales)
  
  * Los gustos personales están relacionados con la identidad (por ejemplo, cuando alguien dice «soy rockero»), pero no necesariamente se corresponden con el consumo cultural (el rockero va más al cine a ver películas de niños porque tiene una hija pequeña). Sin embargo, no dejan de influir en él.
  
  * Dadas tecnologías como la búsqueda semántica o los modelos de lenguaje. Creo que para este caso, la información más conversacional y subjetiva es más útil que, por ejemplo, hacer que seleccione un conjunto de categorías culturales predefinidas (como «música», «teatro», «fiesta»). Además, esta descripción puede actualizarse constantemente para mejorar o afinar este parámetro.

* La selección de ciertos criterios críticos para consumir un producto o experiencia cultural
  
  * Un rango de presupuesto de gasto que le gustaría dedicar a la cultura
  
  * Un rango de días y horas donde sería más probable que asista a un evento o lugar

## C. Modelos de recomendación

Hasta este punto, me parece evidente que estamos ante un problema clásico de sistema de recomendación. [Según](https://en.wikipedia.org/wiki/Recommender_system) [Wikipedia](https://en.wikipedia.org/wiki/Recommender_system) hay dos modos típicos de modelar:

1. Basado en el contenido: En este caso, sería analizar la oferta (tipo de evento, categorías y subcategorías, lugar, hora, precio) y compararlas con las categorías del usuario. Por ejemplo, un evento de música, de qué género y subgénero, en qué lugar, a qué hora, con qué costo, y compararlo con el perfil de cada usuario para asignarle un peso relativo.
   
   1. Desventajas: (1) las categorías iniciales pueden no ser exhaustivas; (2) las categorías necesitan mantenimiento constante por parte de agentes externos al sistema, (3) Las recomendaciones basadas en categorización pueden construir modelos *estereotipados* de los usuarios y la oferta, por tanto, no representar adecuadamente casos atípicos (que podrían ser muchos)
1. Basado en la colaboración de las personas: Este es un mecanismo que utiliza el comportamiento de las personas. Personas con comportamientos similares consumirían cosas similares, así que podemos monitorear su comportamiento de consumo para hacer las recomendaciones; también puede pedírseles que califiquen, prioricen o relacionen ejemplos específicos. Por lo tanto, la retroalimentación puede ser implícita o explícita
   
   1. Desventajas: (1) *cold start*, mientras menos usuarios sobre un ítem, menos datos hay y es más fácil errar; (2) escalabilidad, se necesitan más recursos, ya que los cálculos están ejecutando todo el tiempo conforme se usa el sistema (3) Escasez de ítems, mientras más items de oferta haya, la retroalimentación de los usuarios será más escasa en cada uno

Existen aproximaciones híbridas y también variantes en cada tipo de implementación posible, con el fin de optimizar los resultados. Otros factores importantes pueden ser el grado de apego del sistema a los gustos estrictos del usuario: ¿deberíamos recomendarle algo nuevo que podría gustarle? Si es así, ¿cómo?, ¿con qué frecuencia? Este podría ser un ejemplo del dilema [exploración-explotación](https://en.wikipedia.org/wiki/Exploration-exploitation_dilemma).

# III. Caso práctico: Un sistema de recomendación de eventos culturales para tu ciudad (Mérida como piloto)

## A. Diagramas de sistema

### User Journey Crear cuenta

Al crear su cuenta, el usuario puede elegir si recibir recomendaciones semanales vía Mail, WhatsApp o la web (diseñada principalmente para móvil).

````mermaid
journey
title Crear cuenta
section Landing Page
	Botón rear cuenta: 3: Curioso
section Crea tu cuenta
	Ingresar nombre: 3: Nuevo usuario
	Ingresar descripción de gustos: 5: Nuevo usuario
	Seleccionar dónde recibir recoms.:5 : Nuevo usuario
section Ir a web
	Botón Ir a web: 5: Usuario
	

	
	
````

### User journey de la web App

En la web el usuario podrá explorar sus recomendaciones y compartirlas con otras personas vía WhatsApp o Facebook.

🤑

Eventualmente, el usuario podría hacer cosas más útiles para cerrar su viaje de consumo cultural, como comprar un boleto en la app, añadir el evento a su calendario, invitar al evento a otras personas.

Aquí podría estar el modelo de negocio del sistema, ya que podría cobrarse una comisión por transacción proveniente del sistema, o bien, solicitar fondos del presupuesto de difusión de la cartelera cultural de la ciudad si hay un número suficiente grande de usuarios.

Las interacciones principales de la recomendación

````mermaid
journey
title Web UI
section Login web
	Ingresar user-pass: 3: Usuario
section Ver recomendaciones
	Lista de recomendaciones: 4: Usuario
	Calificar recomendación: 3: Usuario
	Botón detalle recomendación: 5: Usuario
section Recomendación
	Recordarme recomendación: 5: Usuario
	Calificar recomendación: 3:Usuario
	Compartir recomendación: 5: Usuario
section Editar perfil
	Editar nombre: 3: Usuario
	Editar gustos: 5: Usuario
````

### Proceso

Extracción.

El proceso extrae datos de la oferta vía *scrapping* de páginas de Facebook, de páginas de gobierno y de las páginas de los lugares principales que ofertan.

* La data se limpia de inconsistencias, se deduplica y se crean los *embeddings* de las descripciones para la búsqueda semántica

* El perfil del usuario se captura en el momento de creación de su cuenta, posteriormente se crean los *embeddings* de su descripción

Modelo de recomendación

Este proceso usaría una mezcla de los modelos de contenido y colaboración.

Para el MVP el contenido podría probarse a través de una búsqueda semántica entre la descripción de los gustos del usuario y la descripción del evento.

Respecto a la colaboración, se tomarían en cuenta los usuarios con gustos más similares que hayan calificado o asistido a eventos o experiencias que fueran a su vez similares entre sí.

Además, se tomaría en cuenta los eventos que el usuario mismo haya asistido, calificado, comentado o marcado como deseables para recibir recomendaciones similares.

Ambos criterios se ponderarían para seleccionar la lista final de eventos a mostrar.

Salida.

Las recomendaciones en el MVP sería una lista semanal de 1 a *n* (parámetro que el usuario podría modificar en la configuración, por default 10). En la interfaz web, el usuario podría calificar cada recomendación en relación con su posición en la lista (la opción de reordenar la lista podría servir como input para el modelo) y también podría ver el detalle de una recomendación y “calificarla”, esto es:

* Marcar si asistió o asistirá
  
  * Si asistió
    
    * Evaluar de 1 a 5 estrellas
    
    * Comentar qué le pareció
  
  * Si asistirá
    
    * Marcar del 1 al 5 qué tanto le interesan ese tipo de recomendaciones

Si el usuario recibe la lista vía WhatsApp o mail, en esa comunicación habría un botón para que califique las recomendaciones, que lo llevaría a la UI de calificación.

````mermaid
graph TD
    subgraph ETL
        Scrappers --cleaning--> UnifiedSchema
        UserForm --> UserSchema
    end

    subgraph Model
        UnifiedSchema --> Recommender
        UserSchema --> Recommender
    end

    subgraph UI
        Recommender --> RecommendationList
        UserFeedback ----> RecommendationList
    end
````

## C. Evaluación

El primer factor de evaluación sería la retro de las personas dentro de la interfaz web. Debería ser mayoritariamente positiva y en función de ella se harían ajustes sobre cada uno de los subsistemas del modelo.

Adicional a esto, deberían hacerse evaluaciones con usuarios vía entrevistas o user testing para tener una retroalimentación más detallada. Esto es así porque hay un alto grado de subjetividad en los que es una “buena” recomendación, por lo cual entender los criterios del usuario podría ayudar a ponderar mejor los parámetros actuales, añadir nuevos o incluso cambiar total o parcialmente la arquitectura del modelo.
