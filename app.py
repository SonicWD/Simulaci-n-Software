from flask import Flask, render_template, jsonify, request
import pandas as pd
import simpy
import random

app = Flask(__name__)

# Default parameters for simulation
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

data = []

def run_simulation(params):
    global data
    data = []
    
    TIEMPO_LLEGADA_TAREAS = params['TIEMPO_LLEGADA_TAREAS']
    TIEMPO_PLANIFICACION = params['TIEMPO_PLANIFICACION']
    TIEMPO_DESARROLLO = (params['TIEMPO_DESARROLLO_MIN'], params['TIEMPO_DESARROLLO_MAX'])
    TIEMPO_REVISION = params['TIEMPO_REVISION']
    TIEMPO_PRUEBAS = (params['TIEMPO_PRUEBAS_MIN'], params['TIEMPO_PRUEBAS_MAX'])
    TIEMPO_DESPLIEGUE = params['TIEMPO_DESPLIEGUE']
    DURACION_SIMULACION = params['DURACION_SIMULACION']

    env = simpy.Environment()
    planificadores = simpy.Resource(env, 1)
    desarrolladores = simpy.Resource(env, 3)
    revisores = simpy.Resource(env, 1)
    testers = simpy.Resource(env, 2)
    desplegadores = simpy.Resource(env, 1)

    def proceso_tarea(env, id_tarea):
        llegada = env.now

        with planificadores.request() as req:
            yield req
            yield env.timeout(TIEMPO_PLANIFICACION)

        with desarrolladores.request() as req:
            yield req
            tiempo_desarrollo = random.uniform(*TIEMPO_DESARROLLO)
            yield env.timeout(tiempo_desarrollo)

        with revisores.request() as req:
            yield req
            yield env.timeout(TIEMPO_REVISION)

        with testers.request() as req:
            yield req
            tiempo_pruebas = random.uniform(*TIEMPO_PRUEBAS)
            yield env.timeout(tiempo_pruebas)

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

    def generador_tareas(env):
        id_tarea = 0
        while True:
            yield env.timeout(random.expovariate(1.0 / TIEMPO_LLEGADA_TAREAS))
            id_tarea += 1
            env.process(proceso_tarea(env, id_tarea))

    env.process(generador_tareas(env))
    env.run(until=DURACION_SIMULACION)

@app.route('/')
def index():
    return render_template('index.html', params=DEFAULT_PARAMS)

@app.route('/data', methods=['POST'])
def simulation_data():
    params = request.json
    run_simulation(params)
    df = pd.DataFrame(data)
    return jsonify({
        'llegadas': df['llegada'].tolist(),
        'salidas': df['salida'].tolist(),
        'tiempos_ciclo': df['tiempo_ciclo'].tolist()
    })

if __name__ == '__main__':
    app.run(debug=True)
