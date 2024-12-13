from flask import Flask, request, jsonify, render_template
import redis
import json

# Configuración de la base de datos KeyDB
keydb = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

# Crear una instancia de Flask
app = Flask(__name__)

# Ruta para la página principal
@app.route('/')
def home():
    claves = keydb.keys()
    recetas = []
    for clave in claves:
        receta = json.loads(keydb.get(clave))
        recetas.append(receta)
    return render_template('index.html', recetas=recetas)

# Ruta para agregar una receta
@app.route('/recetas', methods=['POST'])
def agregar_receta():
    nombre = request.form.get('nombre')
    ingredientes = request.form.get('ingredientes')
    pasos = request.form.get('pasos')

    if not (nombre and ingredientes and pasos):
        return jsonify({"error": "Faltan datos de la receta"}), 400

    receta = {
        "nombre": nombre,
        "ingredientes": ingredientes,
        "pasos": pasos
    }
    keydb.set(nombre, json.dumps(receta))
    return jsonify({"message": "Receta agregada con éxito."}), 201

# Ruta para actualizar una receta existente
@app.route('/recetas/<nombre>', methods=['GET', 'POST'])
def actualizar_receta(nombre):
    if not keydb.exists(nombre):
        return render_template('error.html', mensaje="Receta no encontrada."), 404

    receta = json.loads(keydb.get(nombre))

    if request.method == 'POST':
        nuevo_nombre = request.form.get("nombre", receta["nombre"])
        nuevos_ingredientes = request.form.get("ingredientes", receta["ingredientes"])
        nuevos_pasos = request.form.get("pasos", receta["pasos"])

        receta["nombre"] = nuevo_nombre
        receta["ingredientes"] = nuevos_ingredientes
        receta["pasos"] = nuevos_pasos

        keydb.delete(nombre)
        keydb.set(receta["nombre"], json.dumps(receta))
        return render_template('success.html', mensaje="Receta actualizada con éxito.")

    return render_template('editar.html', receta=receta)

# Ruta para eliminar una receta existente
@app.route('/recetas/<nombre>/eliminar', methods=['POST'])
def eliminar_receta(nombre):
    if not keydb.exists(nombre):
        return render_template('error.html', mensaje="Receta no encontrada."), 404

    keydb.delete(nombre)
    return render_template('success.html', mensaje="Receta eliminada con éxito.")

# Ruta para buscar una receta por nombre
@app.route('/recetas/<nombre>', methods=['GET'])
def buscar_receta(nombre):
    if not keydb.exists(nombre):
        return render_template('error.html', mensaje="Receta no encontrada."), 404

    receta = json.loads(keydb.get(nombre))
    return render_template('detalle.html', receta=receta)

# Archivo principal de ejecución
if __name__ == '__main__':
    app.run()
