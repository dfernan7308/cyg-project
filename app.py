from flask import Flask, render_template, request, redirect, url_for
import os
import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, template_folder = template_dir)

#Rutas de la aplicación
@app.route('/')
def home():
    search_query = request.args.get('search', '').strip()  # Captura el parámetro 'search' enviado por el formulario
    cursor = db.database.cursor()

    # Si hay un texto en el filtro, buscar en las columnas relevantes
    if search_query:
        sql = """
        SELECT * FROM registro 
        WHERE cliente LIKE %s OR patente LIKE %s OR marca LIKE %s OR modelo LIKE %s 
        OR ano LIKE %s OR kilometraje LIKE %s OR vin LIKE %s 
        OR descripcion LIKE %s OR observacion LIKE %s OR fecha LIKE %s
        """
        like_query = f"%{search_query}%"  # El patrón para buscar en columnas (ignora mayúsculas y minúsculas)
        data = (like_query,) * 10  # Repite el patrón para todas las columnas filtrables
        cursor.execute(sql, data)
    else:
        # Si no hay filtro, traer todos los registros
        cursor.execute("SELECT * FROM registro")

    myresult = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('index.html', data=insertObject)

#Ruta para guardar usuarios en la bdd
@app.route('/user', methods=['POST'])
def addUser():
    patente = request.form['patente']
    cliente = request.form['cliente']
    marca = request.form['marca']
    modelo = request.form['modelo']
    ano = request.form['ano']
    kilometraje = request.form['kilometraje']
    vin = request.form['vin']
    descripcion = request.form['descripcion']
    observacion = request.form['observacion']
    fecha = request.form['fecha']   

    if patente and cliente and marca and modelo and ano and kilometraje and vin and descripcion and observacion and fecha:
        cursor = db.database.cursor()
        sql = "INSERT INTO registro (patente, cliente, marca, modelo, ano, kilometraje, vin, descripcion, observacion, fecha) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        data = (patente, cliente, marca, modelo, ano, kilometraje, vin, descripcion, observacion, fecha)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM registro WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('home'))

@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    patente = request.form['patente']
    cliente = request.form['cliente']
    marca = request.form['marca']
    modelo = request.form['modelo']
    ano = request.form['ano']
    kilometraje = request.form['kilometraje']
    vin = request.form['vin']
    descripcion = request.form['descripcion']
    observacion = request.form['observacion']
    fecha = request.form['fecha']   

    if patente and cliente and marca and modelo and ano and kilometraje and vin and descripcion and observacion and fecha:
        cursor = db.database.cursor()
        sql = "UPDATE registro SET patente = %s, cliente = %s, marca = %s, modelo = %s, ano = %s, kilometraje = %s, vin = %s, descripcion = %s, observacion = %s, fecha = %s WHERE id = %s" 
        data = (patente, cliente, marca, modelo, ano, kilometraje, vin, descripcion, observacion, fecha, id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=4000)