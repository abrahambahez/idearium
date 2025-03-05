
#!/bin/zsh

# Verificar y crear el directorio dist si no existe
if [ ! -d "dist" ]; then
    mkdir dist
else
    # Limpiar contenido existente
    rm -rf dist/*
fi

# Exportar a standard markdown
obsidian-export . --start-at ./ideas/ ./notas

# Limpiar markup de las citas y corchetes escapados
for file in dist/*.md; do
    if [ -f "$file" ]; then
        # Primero reemplazamos los corchetes escapados individuales
        sed -i '' 's/\\\[/[/g; s/\\\]/]/g' "$file"
        # Luego reemplazamos las citas completas
        sed -i '' 's/\[[@]/@/g; s/\\[@/@/g' "$file"
    fi
done

