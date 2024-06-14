from flask import Flask, render_template, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    df = pd.read_csv('resultados_simulacion.csv')
    data = {
        'llegadas': df['llegada'].tolist(),
        'salidas': df['salida'].tolist(),
        'tiempos_ciclo': df['tiempo_ciclo'].tolist()
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
