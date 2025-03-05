# mecanismo de atención artificial

Un mecanismo de atención permite que una [red-neuronal-artificial](red-neuronal-artificial.md) pueda medir la importancia de ciertas características de la información más útiles para completar su tarea. Se compone de:

1. Consulta (Query): Pregunta que describe la tarea
1. Claves (Keys): Características relevantes para la tarea
1. Valores (Values): Información real

La atención se calcula comparando la consulta con las claves. Para cada clave se calcula cuánta importancia tiene para la consulta. Se usan las puntuaciones más altas para pesar los valores. Matemáticamente suelen usarse funciones como la de similitud

En 2017 [@vaswani&al2023](@vaswani&al2023.md) mostraron que los mecanismos de atención eran suficientes para entrenar una [red-neuronal-artificial](red-neuronal-artificial.md) si se usaba una arquitectura de [transformadores-(redes-neuronales)](transformadores-%28redes-neuronales%29.md)
