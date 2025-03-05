# escalar un equipo con kanban

Para escalar el equipo que usa [kanban](kanban.md), @brechner2015 recomienda lo siguiente:

 >
 > The following calculations assume that team capacity grows linearly with team size. However, as Frederick P. Brooks Jr. pointed out in The Mythical Man-Month (1995), cross-team communication grows geometrically with team size. Thus, you can’t double team size and expect double the throughput. Kanban’s focus on smooth flow, visualizing work, and minimal meetings significantly reduces the impact of cross-team communication, but you still need to account for big team changes. Should the following calculations dictate that your team double or triple in size, consider refactoring your project into several teams that work together through a shared architecture and established interfaces. [@brechner2015, cap. 3, sec. Right-size your team]

 >
 > Adding new people to a team always slows it down before it speeds it up.  [@brechner2015, cap. 3, sec. Right-size your team]

Determinar el tamaño del equipo, de acuerdo con @brechner2015:
%% Buscar team size en el libro. Las partes resaltadas deben capturarse a mano para que el resto se calcule%%

|Pending work items|days per month|target start date|target completion date|months|
|------------------|--------------|-----------------|----------------------|------|
|==25==|==30==|==2014-06-01==|==2014-10-01==|4.07|

Crecimiento avanzado del equipo:

|Step|Specify|Implement|Validate|
|----|:-----:|:-------:|:------:|
|A: Average rate per month per person|==6==|==2==|==3==|
|B: Slowest rate (minimum A column)||2||
|C: Numbre of peaople assigned to step B||3||
|D: Throughput of step B (B\*C)||6||
|E: People needed to match B's throughput (D/A)|1|**3**|2|
|F: WIP limits (E\*1.5 rounded up)|2|5|3|
