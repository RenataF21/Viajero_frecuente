# controladores/eventos.py
from flask import render_template, redirect, request, flash, session, url_for
from flask_app.models.viaje import Viaje
from flask_app.models.usuario import Usuario
from datetime import datetime
from flask_app import app


@app.route('/nuevo_viaje', methods=['GET', 'POST'])
def nuevo_viaje():
    if request.method == 'GET':
        return render_template('nuevo.html')
    
    if request.method == 'POST':
        # Crear diccionario con los datos del formulario
        data = {
            'destino': request.form['destino'],
            'organizador': request.form['organizador'],
            'fecha_inicio': request.form['fechaInicio'],
            'fecha_fin': request.form['fechaFin'],
            
        }

        # Validar los datos
        errores = Viaje.validar_viaje(data)
        if errores:
            for error in errores:
                flash(error, 'error')
            return render_template('nuevo.html', data=data)

        # Crear el evento
        viaje_id = Viaje.crear(data)
        if viaje_id:
            flash('viaje creado exitosamente', 'success')
            return redirect(url_for('dashboard'))
        
        flash('Error al crear el viaje', 'error')
        return render_template('nuevo.html', data=data)

@app.route('/ver_viaje/<int:id>')
def ver_viaje(id):
    viaje = Viaje.obtener_por_id(id)
    if not viaje:
        flash('viaje no encontrado', 'error')
        return redirect(url_for('dashboard'))
    
    return render_template('ver_viaje.html', viaje=viaje)

@app.route('/eliminar_viaje/<int:id>')
def eliminar_viaje(id):
    if Viaje.eliminar(id):
        flash('viaje eliminado exitosamente', 'success')
    else:
        flash('Error al eliminar el viaje', 'error')
    return redirect(url_for('dashboard'))


@app.route("/editar_viaje/<int:id>")
def editar_viaje(id):
    if 'usuario_id' not in session:
        return redirect('/login')
    
    viaje = Viaje.obtener_por_id(id)
    if viaje.organizador != session['usuario_id']:
        flash("No tienes permiso para editar este viaje", "error") 
        return redirect(url_for('dashboard'))
    else:
        ##mostrar usuarios que no esten en el evento solamente
        print(viaje)
        return render_template("editar_viaje.html", data=viaje)
    
@app.route("/actualizar_viaje", methods=['POST'])
def actualizar_viaje():
    if 'usuario_id' not in session:
        return redirect('/login')
    
    datos = {
        "id_viaje": request.form['id'],
        'destino': request.form['destino'],
        "organizador": request.form['organizador'],
        "fecha_inicio": request.form['fechaInicio'],
        "fecha_fin": request.form['fechaFin'],
    }
    Viaje.actualizar(datos)

    flash("viaje actualizado exitosamente", "success")
    return redirect(url_for('dashboard'))

