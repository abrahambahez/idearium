# función de atomicidad de un texto

Pienso que el [principio-de-atomicidad-en-la-elaboracion-escrita](principio-de-atomicidad-en-la-elaboracion-escrita.md) puede expresarse lógicamente. Considerando los siguientes componentes:

 > 
 > 1. input: texto (tamaño real *'n'*)
 > 1. valor de un tamaño atómico *'m'*
 > 1. output: texto reducido al tamaño atómico (con una densidad de enlaces *'p'*)
 > 1. Función: input --> elaboración escrita --> output

Cualquier texto de tamaño 'n' puede ser reducido por vía de la elaboración (síntesis cognitiva) y los [vinculos-entre-notas](vinculos-entre-notas.md) a un tamaño cercano al deseado 'm'.

Para mantener la riqueza semántica y detalles importantes, es decir, para que esta reducción no implique pérdida de información valiosa, esta síntesis depende de una característica emergente: la **densidad asociativa**, compuesta de varios niveles, donde el primero es el de la cantidad de enlaces y retroenlaces directos en la nota, y los demás forman un [filtro-de-indireccion-en-sistemas-de-notas](filtro-de-indireccion-en-sistemas-de-notas.md).

La consecuencia de esta función podría implicar que, hipotéticamente, cualquier teoría compleja podría ser expresada en una [nota-atomica](nota-atomica.md) densamente vinculada a múltiples niveles.

---

Algunos garabatos lógicos

````python
input_text: str = "Texto de tamaño n"

def elaborate(input_text):
    atomic_size: int = 300 # words
    
    while len(input_text) != atomic_size:
        output_text = input_text.synthesis().linking()
        return output_text
````
