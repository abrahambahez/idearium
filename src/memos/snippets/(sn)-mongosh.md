# (sn) mongosh
Ya que estás [conectado a un clúster](https://www.freecodecamp.org/espanol/news/tutorial-de-mongodb-atlas-como-empezar/)

Conectarse a una base de datos :: `use <database>` 

Comando base para usar métodos :: `db.<colection>.<method>({<arguments>})`

# Métodos CRUD

Buscar :: `.find({})`
Buscar un registro :: `.findOne({})`
Editar un registro :: `.updateOne({}, { $set: {} })`
Eliminar un registro :: `deleteOne({})`

# Métodos de búsqueda

## Fechas

Filtrar un periodo de dos fechas :: `<dateField>: { $gte: IsoDate("<fecha_inicial>"), $lte: IsoDate("<fecha_final>")}`
