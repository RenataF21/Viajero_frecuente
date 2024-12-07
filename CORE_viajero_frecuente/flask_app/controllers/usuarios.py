from flask import render_template, request, redirect, session, flash
from flask_app import  app, bcrypt
from flask_app.models.usuario import Usuario
from flask_app.models.viaje import Viaje
from datetime import date

# Rutas de la aplicación

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    if 'usuario_id' not in session: 
        return redirect("/")
    viajes = Viaje.get_all()  # Cambia 'viajes' por 'Viaje' para llamar al método de clase correctamente
    usuario = Usuario.get_by_id(session['usuario_id'])
    return render_template(
        "dashboard.html",
        viajes=viajes,
        usuario=usuario
    )

@app.route('/register', methods=['POST'])
def crear_usuario():
    data = {
        'nombre': request.form['name'],
        'apellido': request.form['apellido'],
        'email': request.form['email'],
        'password': request.form['password'],
        'confirmPassword': request.form['confirmPassword']
    }
    if not Usuario.validar_usuario(data):
        return redirect('/')
    else:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            'nombre': request.form['name'],
            'apellido': request.form['apellido'],
            'email': request.form['email'],
            'password': pw_hash
        }
        print(data)
        usuario_id = Usuario.save(data)
        session['usuario_id'] = usuario_id
        return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = Usuario.get_by_email(request.form['loginEmail'])
        print(usuario)
        if usuario and bcrypt.check_password_hash(usuario.password, request.form['loginPassword']):
            session['usuario_id'] = usuario.id
            session['nombre'] = usuario.nombre
            return redirect('/dashboard')
        elif not usuario:
            print("Email inválido")
            flash("Email inválido", "succes")
            return redirect('/')
        else:
            flash("Contraseña inválida", "succes")
            return redirect('/')
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear() #limpia datos de la sesión
    return redirect('/')

