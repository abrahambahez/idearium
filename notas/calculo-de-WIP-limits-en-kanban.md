# cálculo de WIP limits en kanban
Definir los límites del trabajo que se hace, desde la metodología [[kanban]], se pueden calcular tasas que ayuden a fijarlos más objetivamente.

De acuerdo con @brechner2015 [cap. 2, sec. *Step 3: Set limits on chaos*], algunas de esas tasas son:
%% Determine wip limits: Reproducción basada en una imagen del libro. Las marcas amarillas son campos que debes llenar para que el resto se calcule %%

| Step                                           | Specify | Implement | Validate |
| ---------------------------------------------- |:-------:|:---------:|:--------:|
| A: Average rate per month per person           |  ==6==  |   ==2==   |  ==3==   |
| B: Slowest rate (minimum A column)             |         |     2     |          |
| C: Numbre of peaople assigned to step B        |         |   ==3==   |          |
| Throughput of step B (B\*C)                    |         |     6     |          |
| E: People needed to match B's throughput (D/A) |    1    |     3     |    2     |
| F: WIP limits (E\*1.5 rounded up)              |    2    |     5     |    3     |


 >- A On average, each analyst can specify roughly six items per month, each developer can implement roughly two items per month, and each tester can validate roughly three items per month. (Since you’re using ratios here, you could use per week or per day if that’s easier.)
 >- B Implementing was the slowest step (two items per month per person).
 >- C The team had three developers implementing items from the backlog.
 >- D The throughput was six items per month (2 * 3).
 >- E Dividing that throughput by the average rates for each step gives you the people needed for each step to match six items per month (one analyst, three developers, and two testers).
 >- F Adding 50 percent to those people totals and rounding up gives you each step’s WIP limit (2 for Specify, 5 for Implement, and 3 for Validate).
 