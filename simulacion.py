import simpy
import random
import pandas as pd

# Parámetros de la simulación
TIEMPO_LLEGADA_TAREAS = 5  # Tiempo promedio entre llegadas de tareas (en minutos)
TIEMPO_PLANIFICACION = 2  # Tiempo para planificar una tarea (en minutos)
TIEMPO_DESARROLLO = (10, 30)  # Rango de tiempo para desarrollar una tarea (en minutos)
TIEMPO_REVISION = 5  # Tiempo para revisar el código (en minutos)
TIEMPO_PRUEBAS = (5, 15)  # Rango de tiempo para probar una tarea (en minutos)
TIEMPO_DESPLIEGUE = 3  # Tiempo para desplegar una tarea (en minutos)
DURACION_SIMULACION = 480  # Duración de la simulación (en minutos)

# Recursos del equipo
NUM_PLANIFICADORES = 1
NUM_DESARROLLADORES = 3
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
