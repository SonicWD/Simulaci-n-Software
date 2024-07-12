import simpy
import random
import pandas as pd
import sys

# Parámetros de la simulación
TIEMPO_LLEGADA_TAREAS = float(sys.argv[1])
TIEMPO_PLANIFICACION = float(sys.argv[2])
TIEMPO_DESARROLLO = (float(sys.argv[3]), float(sys.argv[4]))
TIEMPO_REVISION = float(sys.argv[5])
TIEMPO_PRUEBAS = (float(sys.argv[6]), float(sys.argv[7]))
TIEMPO_DESPLIEGUE = float(sys.argv[8])
DURACION_SIMULACION = float(sys.argv[9])

# Recursos del equipo
NUM_PLANIFICADORES = 1
NUM_DESARROLLADORES = 5
NUM_REVISORES = 1
NUM_TESTERS = 2
NUM_DESPLIEGADORES = 1

# Datos de la simulación
data = []

# Definición del proceso de una tarea
def proceso_tarea(env, id_tarea, planificadores, desarrolladores, revisores, testers, desplegadores):
    llegada = env.now

    # Planificación
    with planificadores.request() as req:
        yield req
        yield env.timeout(TIEMPO_PLANIFICACION)

    # Desarrollo
    with desarrolladores.request() as req:
        yield req
        tiempo_desarrollo = random.uniform(*TIEMPO_DESARROLLO)
        yield env.timeout(tiempo_desarrollo)

    # Revisión de código
    with revisores.request() as req:
        yield req
        yield env.timeout(TIEMPO_REVISION)

    # Pruebas
    with testers.request() as req:
        yield req
        tiempo_pruebas = random.uniform(*TIEMPO_PRUEBAS)
        yield env.timeout(tiempo_pruebas)

    # Despliegue
    with desplegadores.request() as req:
        yield req
        yield env.timeout(TIEMPO_DESPLIEGUE)

    salida = env.now
    data.append({
        'id_tarea': id_tarea,
        'llegada': llegada,
        'salida': salida,
        'tiempo_ciclo': salida - llegada
    })

# Generador de llegadas de tareas
def generador_tareas(env, planificadores, desarrolladores, revisores, testers, desplegadores):
    id_tarea = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / TIEMPO_LLEGADA_TAREAS))
        id_tarea += 1
        env.process(proceso_tarea(env, id_tarea, planificadores, desarrolladores, revisores, testers, desplegadores))

# Configuración del entorno de simulación
env = simpy.Environment()
planificadores = simpy.Resource(env, NUM_PLANIFICADORES)
desarrolladores = simpy.Resource(env, NUM_DESARROLLADORES)
revisores = simpy.Resource(env, NUM_REVISORES)
testers = simpy.Resource(env, NUM_TESTERS)
desplegadores = simpy.Resource(env, NUM_DESPLIEGADORES)

# Inicialización de la simulación
env.process(generador_tareas(env, planificadores, desarrolladores, revisores, testers, desplegadores))
env.run(until=DURACION_SIMULACION)

# Guardar los datos en un archivo CSV
df = pd.DataFrame(data)
df.to_csv('resultados_simulacion.csv', index=False)
