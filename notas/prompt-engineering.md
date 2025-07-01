# prompt engineering
Leer: https://arxiv.org/abs/2312.16171v1

El concepto de [[prompt]] engineering se refiere a la capacidad de interactuar con un [[LLM]] ([[modelo-de-IA-generativa]]) de forma optimizada para controlar la respuesta que genera. Para esto existen diversas técnicas.

## Principios

Desde el curso de [deeplearning.ai](https://learn.deeplearning.ai/chatgpt-prompt-eng/lesson/1/introduction)

### Escribir instrucciones claras y específicas

Algunas tácticas usadas para la claridad son:

#### Delimitadores

Dejar claro al modelo que hay secciones separadas usando caracteres específicos y diciendo explícitamente

- Dado un texto rodeado por 'comillas simples'
- Prompt: Resume el texto rodeado por comillas simples
- Esto ayuda a evitar las *prompt injections*

#### Solicitar salidas estructuradas
Prompt: *Generate a list of three made-up book titles along with their authors and genres. Provide them in JSON format with the following keys: book_id, title, author, genre.*

#### Validar que las condiciones sean satisfechas
Validar asunciones necesarias para hacer la tarea. Prompt:

You will be provided with text delimited by triple quotes. If it contains a sequence of instructions, re-write those instructions in the following format:
Step 1 - ...
Step 2 - …
…
Step N - …
If the text does not contain a sequence of instructions, then simply write \"No steps provided.\"

#### Prompting de muestras
Dar ejemplos de tareas correctas; luego pedir al modelo hacer la tarea. Prompt:

```python
prompt = f"""
Your task is to determine if the student's solution \
is correct or not.
To solve the problem do the following:
- First, work out your own solution to the problem. 
- Then compare your solution to the student's solution \ 
and evaluate if the student's solution is correct or not. 
Don't decide if the student's solution is correct until 
you have done the problem yourself.

Use the following format:
Question:
[question here]
Student's solution:

[student's solution here]

Actual solution:

[steps to work out the solution and your solution here]

Is the student's solution the same as actual solution \
just calculated:

[yes or no]

Student grade:

[correct or incorrect]


Question:
[
I'm building a solar power installation and I need help \
working out the financials. 
- Land costs $100 / square foot
- I can buy solar panels for $250 / square foot
- I negotiated a contract for maintenance that will cost \
me a flat $100k per year, and an additional $10 / square \
foot
What is the total cost for the first year of operations \
as a function of the number of square feet.
]
Student's solution:
[
Let x be the size of the installation in square feet.
Costs:
1. Land cost: 100x
2. Solar panel cost: 250x
3. Maintenance cost: 100,000 + 100x
Total cost: 100x + 250x + 100,000 + 100x = 450x + 100,000
]
Actual solution:
"""
```

### Dar tiempo al modelo para pensar

#### Especificar pasos para cumplir una tarea

```python
text = f"""
In a charming village, siblings Jack and Jill set out on \ 
a quest to fetch water from a hilltop \ 
well. As they climbed, singing joyfully, misfortune \ 
struck—Jack tripped on a stone and tumbled \ 
down the hill, with Jill following suit. \ 
Though slightly battered, the pair returned home to \ 
comforting embraces. Despite the mishap, \ 
their adventurous spirits remained undimmed, and they \ 
continued exploring with delight.
"""
# example 1
prompt_1 = f"""
Perform the following actions: 
1 - Summarize the following text delimited by triple \
backticks with 1 sentence.
2 - Translate the summary into French.
3 - List each name in the French summary.
4 - Output a json object that contains the following \
keys: french_summary, num_names.

Separate your answers with line breaks.

Text:
```{text}```"""
```

Instruir al modelo para trabajar su propia solución antes de llegar a una conclusión:

```python
prompt = f"""
Your task is to determine if the student's solution \
is correct or not.
To solve the problem do the following:
- First, work out your own solution to the problem. 
- Then compare your solution to the student's solution \ 
and evaluate if the student's solution is correct or not. 
Don't decide if the student's solution is correct until 
you have done the problem yourself.

Use the following format:
Question:

question here

Student's solution:

student's solution here

Actual solution:

steps to work out the solution and your solution here

Is the student's solution the same as actual solution \
just calculated:

yes or no

Student grade:
correct or incorrect


Question:

I'm building a solar power installation and I need help \
working out the financials. 
- Land costs $100 / square foot
- I can buy solar panels for $250 / square foot
- I negotiated a contract for maintenance that will cost \
me a flat $100k per year, and an additional $10 / square \
foot
What is the total cost for the first year of operations \
as a function of the number of square feet.
 
Student's solution:

Let x be the size of the installation in square feet.
Costs:
1. Land cost: 100x
2. Solar panel cost: 250x
3. Maintenance cost: 100,000 + 100x
Total cost: 100x + 250x + 100,000 + 100x = 450x + 100,000

Actual solution:
"""
```

## Procesos iterativos

Se trata de refinar el proceso de prompting. Probar varias peticiones hasta ver la que mejor funcione.

- Probar un prompt inicial
- Analizar dónde falla el resultado
- Clarificar respuestas, dar más tiempo para pensar
- Refinar prompts con un grupo de ejemplos

## Resumir

Dar contexto. Controlar extensión, enfocarse en tópicos específicos.

Tipos de resumen. Para cada extensión de texto a resumir hay diferentes estrategias. Particularmente usando [langchain](https://python.langchain.com/en/latest/index.html)

- Oraciones: usar un prompt simple
- Párrafos: usar [prompt templates](https://python.langchain.com/en/latest/modules/prompts/prompt_templates.html)
- Páginas: usar estrategias como [map_reduce](https://python.langchain.com/en/latest/modules/chains/index_examples/qa_with_sources.html?highlight=map_reduce#the-map-reduce-chain)
- Un libro entero: usar [embeddings](https://python.langchain.com/en/latest/reference/modules/embeddings.html?highlight=embeddings)

## Inferencia

Extraer etiquetas, nombres, sentimientos, temas, etcétera. Ejemplo:

```python
prompt = f"""
Identify the following items from the review text: 
- Item purchased by reviewer
- Company that made the item

The review is delimited with triple backticks. \
Format your response as a JSON object with \
"Item" and "Brand" as the keys. 
If the information isn't present, use "unknown" \
as the value.
Make your response as short as possible.
  
Review text: '''{lamp_review}'''
"""
```

## Transformación

Tareas como traducir, gramática, ortografía, tono, voz, conversión de formatos (p.e. html a json)

## Expansión

Toma un prompt pequeño y lo amplía. Puede generar texto novedoso a partir de ejemplos e instrucciones. El nivel de temperatura (*temperature*) es relevante para determinar qué tanto diverge de la predicción de la cadena de texto.
