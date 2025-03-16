# árbol de oportunidad-solución
Propuesto por [[@torres2021]] como un modelo para implementar el [[descubrimiento continuo de producto]]. Estructura los conceptos básicos que ordenan la investigación constante. En abstracto:

```mermaid
flowchart TD

A("Outcome") --> B1("Oportunity")
A --> B2("Oportunity")
A --> B3("Oportunity")
B1 --> B1a("Oportunity")
B1 --> B1b("Oportunity")
B1a --> C1["Solution"]
B1a --> C2["Solution"]
C1 --> D1{{"Assumption Test"}}
C1 --> D1a{{"Assumption Test"}}
C2 --> D2{{"Assumption Test"}} & D1a
```

Es trabajo del *Product Manager ordenar* las oportunidades descubiertas en una estructura coherente donde puedan relacionarse. [[@torres2021]] [cap. 6] da algunos ejemplos:

```mermaid
flowchart LR

B1("I can't\nfind anything\nto watch")
B1 --> B1a("I'm out of episodes\nof my favorite shows")
B1 --> B1b("I can't figure out how to search \nfor a specific show")
B1 --> B1c("The show I was watching\n is no longer available")
```

