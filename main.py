import json

# Módulos de mi proyecto
from services.monitor_olimpica import monitor_olimpica
from services.monitor_jumbo import monitor_jumbo
from services.monitor_cruzverde import monitor_cruzverde
from services.monitor_farmatodo import monitor_farmatodo

diccionario_productos_cruzverde = monitor_cruzverde()
# monitor_olimpica(diccionario_productos_cruzverde)
# monitor_jumbo()
monitor_farmatodo(diccionario_productos_cruzverde)

print("Fin ejecución.")