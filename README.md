# Prototipo de zettelkasten v5

Este repositorio es una prueba de un nuevo zettelkasten. Con él, estoy tratando de [abandonar Obsidian](https://sabhz.com/diciendo-adios-a-obsidian) y, con ello, migrando a una nueva lógica de trabajo con notas.

Primero, revisa el [Manual de estilo](manual-de-estilo.md).

Luego, estas son algunas de las reglas que puede tener:

- **Centrado en la prosa**. No *frontmatter* ni cosas que tiendan a estructurar más allá del lenguaje natural
    - Volver al markdown más estandarizado
- **Escritura desde la terminal**: Neovim, zk, flujo de trabajo de escritorio inspirado por el estilo [*Docs as code*](https://www.writethedocs.org/guide/docs-as-code/)
    - La obsesión por aumentar el zettelkasten desde el móvil/celular es ociosa e inútil. Este es trabajo intelectual estilo *Deepwork*
- ID con slug: el punto medio entre encontrar notas con el sistema de archivos y tener enlaces semánticos indexados. Hacia atrás, las notas coinciden con sus títulos, hacia adelante sería más bien una serie de palabras clave o un resumen del título
- **Centrado en Git**: Como estoy pensando en el escritorio y la terminal, cada sesión de trabajo debe ser llevada por Git, como debe ser.
- Pensar más en scripts o CLI que en UI con *Plugins*

## Anatomía de una nota

1. ID slug con palabras clave, parecido a la idea de [nombre de archivo como el *endpoint* de una API](https://notes.andymatuschak.org/Evergreen_note_titles_are_like_APIs)
2. Un único título H1 al principio de cada nota, estilo `#`, esta es la base de la búsqueda.
3. Contenido prosa y markdown. Siguiendo la lógica de una nota atómica y el estilo de un micro-ensayo.
4. Densamente vinculado
5. Los links son wikilinks, ya que la estrategia del slug produce nombres de archivo muy variables en extensión, y sería redundante, además de ocupar mucho espacio, repetir título y nombre de archivo en el estilo de enlace markdown estándar.

## Notas de referencia

- Tienen como nombre de archivo su *@citekey* y una plantilla específica centrada en la prosa, no en los metadatos (para eso uso Zotero)
- Su contenido puede ser más largo

## Puntos de partida

Me interesa pensar en soluciones a esos problemas en términos de [prototipar utopías](./notas/prototipar-utopias.md).


