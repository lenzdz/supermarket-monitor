import json

# Módulos de mi proyecto
from services.monitor_olimpica import monitor_olimpica
from services.monitor_jumbo import monitor_jumbo
from services.monitor_cruzverde import monitor_cruzverde

diccionario_productos_cruzverde = monitor_cruzverde()
monitor_olimpica(diccionario_productos_cruzverde)
monitor_jumbo()

print("Fin ejecución.")