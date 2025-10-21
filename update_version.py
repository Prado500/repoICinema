# update_version.py - Script para modificar automáticamente la versión
import re
import sys

def update_version_file(new_color):
    with open('app/main.py', 'r') as file:
        content = file.read()
    
    # Buscar y reemplazar el mensaje de color
    old_pattern = r'"feature": "Color: [A-Z]+"'
    new_feature = f'"feature": "Color: {new_color}"'
    
    content = re.sub(old_pattern, new_feature, content)
    
    with open('app/main.py', 'w') as file:
        file.write(content)
    
    print(f"✅ Color cambiado a: {new_color}")

if __name__ == "__main__":
    colors = ["ROJO", "VERDE", "AZUL", "AMARILLO", "NARANJA"]
    build_id = sys.argv[1] if len(sys.argv) > 1 else "1"
    color_index = int(build_id) % len(colors)
    update_version_file(colors[color_index])