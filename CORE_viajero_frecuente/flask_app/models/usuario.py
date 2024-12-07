from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NOMBRE_REGEX = re.compile(r'^[a-zA-Z\s]+$')
DATABASE = 'esquema_viajeros'


class Usuario:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM usuarios;"
        resultados = connectToMySQL(DATABASE).query_db(query)
        usuarios = []
        for usuario in resultados:
            usuarios.append(cls(usuario))
        return usuarios

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO usuarios (nombre, apellido, email, password, created_at , updated_at) 
        VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s, NOW(), NOW());
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        resultado = connectToMySQL(DATABASE).query_db(query, {'email': email})
        if len(resultado) < 1:
            return False
        return cls(resultado[0])

    @classmethod
    def get_by_id(cls, id):
        query = "SELECT * FROM usuarios WHERE id_usuario = %(id)s;"
        resultado = connectToMySQL(DATABASE).query_db(query, {'id': id})
        if not resultado:
            return False
        return cls(resultado[0])

    @staticmethod
    def validar_usuario(usuario):
        is_valid = True
        #VALIDACION NOMBRE
        if len(usuario['nombre']) <= 0:
            flash("El nombre no puede estar vacío.", "danger")
            is_valid = False
        if len(usuario['nombre']) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "danger")
            is_valid = False
        else:
            if not NOMBRE_REGEX.match(usuario['nombre']):
                flash("El nombre solo puede contener letras.", "danger")
                is_valid = False
        #VALIDACION APELLIDO
        if len(usuario['apellido']) < 2:
            flash("El apellido debe tener al menos 2 caracteres.", "danger")
            is_valid = False
        #VALIDACION EMAIL
        if not EMAIL_REGEX.match(usuario['email']):
            flash("Email inválido.", "danger")
            is_valid = False
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        data = {'email': usuario['email']}
        resultado = connectToMySQL(DATABASE).query_db(query, data)
        if len(resultado) > 0:
            flash("El email ya está registrado.", "danger")
            is_valid = False
        #VALIDACION PASSWORD
        if len(usuario['password']) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "danger")
            is_valid = False
        if len(usuario['password']) <= 0:
            flash("La contraseña no puede estar vacía.", "danger")
            is_valid = False
        #VALIDACION CONFIRMACION PASSWORD
        if len(usuario['confirmPassword']) <= 0:
            flash("La confirmación de la contraseña no puede estar vacía.", "danger")
            is_valid = False
        if (usuario['password'] != usuario['confirmPassword']):
            flash("Las contraseñas no coinciden.", "danger")
            is_valid = False
        return is_valid
