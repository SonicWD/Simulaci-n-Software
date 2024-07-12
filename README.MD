# Proyecto de Simulación y Ejecución

Este proyecto incluye aplicaciones y scripts para simulación y ejecución en Python.

## Instrucciones de Clonación y Ejecución

### Clonación del Repositorio

Para clonar este repositorio a tu máquina local, usa el siguiente comando:

```bash
git clone https://github.com/SonicWD/Simulaci-n-Software
cd Simulacion Software
```
# Configuración del Entorno Virtual

Es recomendable utilizar un entorno virtual para gestionar las dependencias del proyecto. A continuación, se muestra cómo activar un entorno virtual en diferentes sistemas operativos:

## Windows

```bash
.\.venv\Scripts\activate
```
## Ejecución de la Aplicación Principal
Para ejecutar la aplicación principal (app.py), usa el siguiente comando:

```bash
python app.py
```
## Ejecución del Script de Simulación
Para ejecutar el script de simulación (simulacion.py) con los parámetros específicos (ejemplo: 10 2 10 30 5 5 15 3 100), utiliza el siguiente comando:

```bash
python simulacion.py 10 2 10 30 5 5 15 3 100
```
El script simulacion.py es un simulador que modela un proceso de desarrollo de software utilizando el módulo SimPy en Python. Las entradas que se le proporcionan al ejecutarlo (python simulacion.py 10 2 10 30 5 5 15 3 100) son parámetros que configuran la simulación. Aquí te explico qué representa cada uno de estos parámetros, ya para cambiar los parametros de los recuersos humanos directamente desde el codigo donde estan las varibles inicializadas:

### TIEMPO_LLEGADA_TAREAS: Este parámetro determina la tasa promedio de llegada de nuevas tareas al sistema. Es decir, cuánto tiempo, en promedio, pasa entre la llegada de una tarea y la siguiente.

### TIEMPO_PLANIFICACION: Es el tiempo que tarda en realizarse la planificación de una tarea una vez que se le asigna a un planificador.

### TIEMPO_DESARROLLO: Es un rango de tiempo (representado como una tupla) que indica el tiempo mínimo y máximo que puede tomar el desarrollo de una tarea.

### TIEMPO_REVISION: Es el tiempo que toma la revisión del código de una tarea una vez que ha sido desarrollada.

### TIEMPO_PRUEBAS: Es un rango de tiempo (representado como una tupla) que indica el tiempo mínimo y máximo que pueden tomar las pruebas de una tarea.

### TIEMPO_DESPLIEGUE: Es el tiempo que toma el despliegue de una tarea una vez que ha pasado las pruebas y está lista para ser implementada.

### DURACION_SIMULACION: Es el tiempo total de simulación, es decir, por cuánto tiempo se simulará el proceso de desarrollo de software.