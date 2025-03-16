# Agile project management with Kanban
Brechner y Waletzky (2015)

## Proceso de [[kanban]]

1. Definir **el flujo** (la rutina de alto nivel del equipo): el flujo más abstracto es el clásico *to do, doing, done*, en el libro: *backlog, specify, implement, validate*.
2. Redecorar la pared
3. Poner límites al caos
4. Definir lo “hecho”. De ahí que algunos pasos se dividen en dos columnas (una para el *doing* y otra para el *done*), la definición de hecho se hace en equipo para cada paso
5. Hacer daily standup. Los standups diarios se hacen sobre el tablero

### WIP Limit (Limitar el trabajo que se está haciendo)

#### Definir un WIP Limit inicial

> Start with setting the WIP limit for your slowest step to the number of team members doing that step, plus a 50 percent buffer. That always keeps the slowest step busy yet still limits the number of note cards at that step.
>
> Then use ratios to set the WIP limits for the other steps so that their throughput matches the slowest step.
> 
>The result is starting values that you can continually adjust as needed to maximize throughput. (Capítulo 2)


Los items que están en la columna *done* cuentan para el límite porque contribuyen a sus efectos positivos sobre la velocidad de entrega.

### Standup

Dado que kanban es una metodología *pull*, los standups inician en el último paso del flujo para liberar espacios qué jalar hacia la derecha. La pregunta es *¿Qué items están hechos de el ‘nombre del último paso’?*. Si hay espacio para jalar tareas que estén hechas del paso anterior (y hay que validar que sí estén hechas preguntando *¿Qué hicieron para considerarlas hechas?*), se deciden jalar tantas como espacios haya.

Así se repite el ciclo en cada paso. Algunas tareas se pueden partir en tareas más pequeñas (y cuentan como una, la original, en términos del *WIP Limit*).

Antes de terminar se pregunta *¿debemos cambiar el orden del backlog debido a nuevas peticiones o requerimeintos?* y finalmente se pregunta *¿alguien necesita ayuda extra?*.

Si una persona termina y no puede jalar items debido al *WIP Limit*, puede ofrecerse a ayudar en tareas donde se requiera apoyo. Si un paso está listo para jalar items pero el paso anterior no tiene items terminados es el mismo caso.

>He could specify the next item from the backlog, but doing that isn’t helpful; it just creates more work for the team to implement, and the team is already at its implementation limit. The team can’t go any faster without help. Yes, the next item in the backlog may eventually need to be specified, but that only hides this issue until later, doesn’t help solve the problem, and may even result in work being thrown away if priorities change. (Capítulo 2)

Si no hay manera en que la persona bloqueada pueda ayudar a liberar el espacio del siguiente paso, puede proactivamente buscar otra clase de trabajo productivo: *«he can still be productive by getting a head start on customer research, advanced planning, or new tooling. There’s always productive work available that doesn’t hurt the team»*.

#### Cualquier disturbio en el flujo de trabajo requiere diagnóstico e intervención

>If team members or work items often seem to be blocked, your team may need to adjust the Specify step, WIP limits, staff assignments, or other variables. The proper action to take depends on the symptoms. (cap. 2)

### Items que se bloquean porque requieren input externo

Se puede añadir una columna más al paso (además de *haciendo* y *hecho*) que sería *en seguimiento*. Cuando un ítem entra ahí deja de contar para el WIP Limit hasta que el input externo llega, en ese momento se puede mover a *haciendo* sólo si hay espacio disponible. Si no hay input durante mucho tiempo, puede moverse al *icebox* o *parking lot*.

### Tratamiento de bugs

Cuando un bug lleva tanto trabajo como cualquier item, se debe manejar como tal. Eso implica integrarlo al resto del backlog y al flujo natural.
## Varios flujos Kanban en un sólo tablero

También llamados *swimlanes* o *pipelines*, un sólo tablero puede contener varios de estos flujos. Cada uno tiene sus propios pasos (columnas) con sus propios WIP limits y reglas de hecho. Se visualizan de forma vertical, uno debajo de otro, sólo coincidiendo en los pasos de compromiso y entrega (el primero de trabajo y el último, de hecho)

![multiple-swimlines](https://www.3cs.ch/wp-content/uploads/kanban-board-operations-with-swimlanes.png)

## Manejo de fechas

La filosofía de Kanban es el *continous delivery* de valor. No hay ceremonias específicas pero las estimaciones pueden hacerse a través de ciertas técnicas:

- *Planning poker*
- *Task completion rate*
- >*Calculate your task completion rate. To do this, count the number of tasks that are done with their final step within any two-week to four-week period, and divide by the number of days. (For teams that average around three days per task, like mine, a sample of two to four weeks should be sufficient.) Note that the task completion rate isn’t the reciprocal of the average time required to complete a task (the task’s cycle time). That’s because the task completion rate accounts for all team members and all steps (including the Specify step, which breaks down items of variable size into tasks of similar size).*


>The estimating formula used (pending tasks divided by the task completion rate) calculates what’s often referred to as “lead time.” This concept is derived from Little’s Law, which states that the work in progress in a system (pending tasks) is equal to the average system throughput (task completion rate) multiplied by the system response time (lead time). (Cap. 3)

#### KPI de estimación de tareas

>  Task completion rate (TCR) You can track TCR as a moving average or monthly updated value (tasks completed per day). Doing so helps account for delays and changing team dynamics.
> 
>  Current task estimate (CTE) This is the total number of active tasks and estimated pending tasks (including tasks in a Track column). The CTE is essential for updated estimates because it represents remaining work.
> 
>  Task add rate (TAR) This value wasn’t used in the previous section because it measures changes in plans, not initial estimates. You subtract the total number of tasks (pending, active, and done) at the start of a month from the total number at the end and divide by the number of days. This gives you the tasks added per day (or tasks cut if the value is negative) and accounts for plan changes and feature bloat. (Cap. 3)

Con estas métricas es posible calcular la **fecha esperada de término** (*expected completion rate*):


### El problema de crecer el equipo y cómo calcularlo

> The following calculations assume that team capacity grows linearly with team size. However, as Frederick P. Brooks Jr. pointed out in The Mythical Man-Month (1995), cross-team communication grows geometrically with team size. Thus, you can’t double team size and expect double the throughput. Kanban’s focus on smooth flow, visualizing work, and minimal meetings significantly reduces the impact of cross-team communication, but you still need to account for big team changes. Should the following calculations dictate that your team double or triple in size, consider refactoring your project into several teams that work together through a shared architecture and established interfaces.

Para determinar el tamaño del equipo necesario para cumplir una fecha de acuerdo con un número de tareas dado, necesito calcular primero el tiempo


Después puedo usar algunos indicadores más para estimar el tamaño


#### Aproximación avanzada

If you have the current task estimate (CTE), task add rate (TAR), and task completion rate (TCR), as described in the “Track expected completion date” section, you can estimate the proper team size with a bit more confidence.


For a comparison with the basic approach, I set the current task estimate to 100 (four tasks per basic-example work item), used the task add rate and task completion rate from the previous section, and the same 4.07 month period as for the basic example (122 days). I use days instead of months because task add rate and task completion rate are measured in days.

The estimated number of days needed to complete 100 tasks is 152, but the number of days available is 122. The ratio between the estimated and expected number of days is 152 / 122 = 1.24—that’s the multiple of team members we need.


## Ingeniería sostenida

Para gestionar errores, *bugs* o dar mantenimiento a productos se puede crear un tablero de ingeniería sostenida, gestionado por un equipo
