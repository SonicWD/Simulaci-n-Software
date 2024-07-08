from flask import Flask, render_template, jsonify, request  
import pandas as pd  
import simpy  
import random 

app = Flask(__name__)  # Crear una instancia de la aplicación Flask saque 80 lptm

# Parámetros predeterminados para la simulación
DEFAULT_PARAMS = {
    'TIEMPO_LLEGADA_TAREAS': 5,
    'TIEMPO_PLANIFICACION': 2,
    'TIEMPO_DESARROLLO_MIN': 10,
    'TIEMPO_DESARROLLO_MAX': 30,
    'TIEMPO_REVISION': 5,
    'TIEMPO_PRUEBAS_MIN': 5,
    'TIEMPO_PRUEBAS_MAX': 15,
    'TIEMPO_DESPLIEGUE': 3,
    'DURACION_SIMULACION': 480
}

data = []  # Lista para almacenar los datos de la simulación

def run_simulation(params):
    """
    Función para ejecutar la simulación del proceso de desarrollo de software.
    
    Args:
    - params (dict): Diccionario con los parámetros de simulación.
    """
    global data  # Acceder a la lista de datos global
    
    data = []  # Reiniciar la lista de datos
    
    # Extraer parámetros del diccionario de entrada
    TIEMPO_LLEGADA_TAREAS = params['TIEMPO_LLEGADA_TAREAS']
    TIEMPO_PLANIFICACION = params['TIEMPO_PLANIFICACION']
    TIEMPO_DESARROLLO = (params['TIEMPO_DESARROLLO_MIN'], params['TIEMPO_DESARROLLO_MAX'])
    TIEMPO_REVISION = params['TIEMPO_REVISION']
    TIEMPO_PRUEBAS = (params['TIEMPO_PRUEBAS_MIN'], params['TIEMPO_PRUEBAS_MAX'])
    TIEMPO_DESPLIEGUE = params['TIEMPO_DESPLIEGUE']
    DURACION_SIMULACION = params['DURACION_SIMULACION']

    env = simpy.Environment() 
    planificadores = simpy.Resource(env, 1)  # Recurso para la planificación
    desarrolladores = simpy.Resource(env, 3)  # Recurso para el desarrollo se puede cambiar(3 desarrolladores)
    revisores = simpy.Resource(env, 1)  # Recurso para la revisión
    testers = simpy.Resource(env, 2)  # Recurso para las pruebas (2 testers)
    desplegadores = simpy.Resource(env, 1)  # Recurso para el despliegue

    def proceso_tarea(env, id_tarea):
        """
        Función para simular el proceso de una tarea de software.
        
        Args:
        - env (simpy.Environment): Entorno de SimPy para manejar la simulación.
        - id_tarea (int): Identificador único de la tarea.
        """
        llegada = env.now  # Momento de llegada de la tarea

        # Etapa de planificación
        with planificadores.request() as req:
            yield req
            yield env.timeout(TIEMPO_PLANIFICACION)

        # Etapa de desarrollo
        with desarrolladores.request() as req:
            yield req
            tiempo_desarrollo = random.uniform(*TIEMPO_DESARROLLO)  # Tiempo de desarrollo aleatorio
            yield env.timeout(tiempo_desarrollo)

        # Etapa de revisión
        with revisores.request() as req:
            yield req
            yield env.timeout(TIEMPO_REVISION)

        # Etapa de pruebas
        with testers.request() as req:
            yield req
            tiempo_pruebas = random.uniform(*TIEMPO_PRUEBAS)  # Tiempo de pruebas aleatorio
            yield env.timeout(tiempo_pruebas)

        # Etapa de despliegue
        with desplegadores.request() as req:
            yield req
            yield env.timeout(TIEMPO_DESPLIEGUE)

        salida = env.now  # Momento de salida de la tarea
        tiempo_ciclo = salida - llegada  # Tiempo total de ciclo de la tarea

        # Agregar datos de la tarea a la lista
        data.append({
            'id_tarea': id_tarea,
            'llegada': llegada,
            'salida': salida,
            'tiempo_ciclo': tiempo_ciclo
        })

    def generador_tareas(env):
        """
        Función para generar continuamente tareas de software según un intervalo de llegada.
        
        Args:
        - env (simpy.Environment): Entorno de SimPy para manejar la simulación.
        """
        id_tarea = 0  # Inicializar el ID de la tarea
        while True:
            yield env.timeout(random.expovariate(1.0 / TIEMPO_LLEGADA_TAREAS))  # Intervalo de llegada aleatorio
            id_tarea += 1  # Incrementar el ID de la tarea
            env.process(proceso_tarea(env, id_tarea))  # Iniciar el proceso de la nueva tarea

    # Agregar el generador de tareas al entorno de simulación
    env.process(generador_tareas(env))
    env.run(until=DURACION_SIMULACION)  # Ejecutar la simulación hasta el tiempo máximo

@app.route('/')
def index():
    """
    Ruta principal para renderizar la plantilla HTML con parámetros predeterminados.
    """
    return render_template('index.html', params=DEFAULT_PARAMS)

@app.route('/data', methods=['POST'])
def simulation_data():
    """
    Ruta para manejar la solicitud POST con los parámetros de simulación y devolver los datos de la simulación.
    """
    params = request.json  # Obtener los parámetros de simulación del cuerpo JSON de la solicitud
    run_simulation(params)  # Ejecutar la simulación con los parámetros recibidos
    df = pd.DataFrame(data)  # Crear un DataFrame con los datos de la simulación
    # Devolver los datos de simulación en formato JSON
    return jsonify({
        'llegadas': df['llegada'].tolist(),  # Convertir la columna 'llegada' a lista
        'salidas': df['salida'].tolist(),  # Convertir la columna 'salida' a lista
        'tiempos_ciclo': df['tiempo_ciclo'].tolist()  # Convertir la columna 'tiempo_ciclo' a lista
    })

if __name__ == '__main__':
    app.run(debug=True)  # Ejecutar la aplicación Flask en modo debug si se ejecuta como script principal
