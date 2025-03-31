# optimizar Gmail para trabajar con clientes

## Mantenimiento adecuado del inbox

Para usar mejor el email como herramienta de trabajo es indispensable mantener un orden.

- Limpieza automática con [CleanFox](https://www.cleanfox.io/)
- Marcar con estrella los mensajes de clientes, cada X tiempo seleccionar todos los que no están marcados y eliminarlos. Esto creará una vista más limpia de los mensajes

## Automatización de grupos de stakeholders con filtros y etiquetas

“Grupo de stakeholders” Significa un grupo de personas relacionadas con un proyecto, cliente o contrato. En el caso del mail, el grupo se compone de personas que tienen nombres y correos.

Es posible crear un filtro donde pongamos todos los correos de un grupo de stakeholders y asignarles automáticamente una etiqueta (idealmente el nombre del proyecto o producto). Para hacer esto:

- Entrar a Gmail
- Ir a ajustes > todos los ajustes > Filtros y direcciones bloqueadas
- Seleccionar Crear un filtro
- El filtro debe tener la forma `from:(name@email | name@email | …)` lo que indica que filtramos todos los correos que vengan de cualquiera de esas direcciones
- Dar continuar (aunque salgan advertencias)
- Asociar la acción del filtro a asignar una etiqueta, crearla si no existe, la etiqueta debería llamarse como conozcamos mejor al grupo de stakeholders (p.e. SIUCAM, Twitch, etcétera)
- Listo, cada que llegue un correo de esa lista de emails tendrá asociada la etiqueta y podremos filtrar
- Si llegan nuevos stakeholders al grupo hay que actualizar el filtro y así

## Estrategia de comunicación por grupos de stakeholders

Cada grupo de stakeholders debería tener un guideline de comunicación con hacks relevantes sobre el cliente, proyecto, estilo de comunicación, etcétera.

Familiarizarse con el perfil es muy importante.

## Técnicas específicas

### Convertir correos relevantes en tareas
[Ejemplo con Linear](https://linear.app/docs/creating-issues#create-an-issue-via-email)

También se puede con Google Tasks, y con otras aplicaciones.

Esto es útil para accionar peticiones que requieran tareas del equipo e integrarlas a algún flujo de trabajo

### Convertir correos en comunicación de proyecto con la integración Mail-Slack

También es posible publicar el contenido de un correo en un canal de Slack, con el fin de compartir feedback o información relevante para un proyecto directamente.

### Hacia un sistema unificado de relación con clientes para productos

Ver [[relaciones con cliente en texto plano]]

El propósito es usarlo como base para diversas operaciones y relaciones con cliente. Este CRM no es solamente un pipeline de ventas, sino que debería ayudarnos a automatizar acciones de [[descubrimiento continuo de producto]], como parte de [[técnica de descubrimiento de producto]].

