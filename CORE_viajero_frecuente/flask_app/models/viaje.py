# models/viaje.py
from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
DATABASE = 'esquema_viajeros'
class Viaje:
    def __init__(self, data):
        self.id_viaje = data['id']
        self.destino = data['destino']
        self.organizador = data['organizador']
        self.fecha_inicio = data['fecha_inicio']
        self.fecha_fin = data['fecha_fin']
        self.acciones = data['acciones']
        self.id_organizador = data['id_organizador']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.organizador = data.get('organizador', None)  # Para joins con la tabla usuarios

    @classmethod
    def get_all(cls):
        query = """
            SELECT v.*, u.nombre as organizador 
            FROM viajes v
            JOIN usuarios u ON v.id_organizador = u.id_usuario
            ORDER BY v.fecha_inicio;
        """
        results = connectToMySQL(DATABASE).query_db(query)
        viajes = []
        if results:
            for row in results:
                viajes.append(cls(row))
        return viajes
    
    
    @classmethod
    def crear(cls, data):
        query = """
            INSERT INTO viajes (destino, organizador, fecha_inicio, fecha_fin, acciones, id_organizador)
            VALUES (%(destino)s, %(organizador)s, %(fecha_inicio)s, %(fecha_fin)s %(acciones)s, %(id_organizador)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def actualizar(cls, data):
        query = """
            UPDATE viajes 
            SET destino = %(destino)s,
                organizador = %(organizador)s,
                fecha_inicio = %(fecha_inicio)s,
                fecha_fin = %(fecha_fin)s,
                acciones = %(acciones)s
            WHERE id_viaje = %(id_viaje)s;
        """
        
        return connectToMySQL(DATABASE).query_db(query, data)


    @classmethod
    def obtener_por_id(cls, id_viaje):
        query = """
            SELECT v.*, u.nombre as organizador 
            FROM viajes v
            JOIN usuarios u ON v.id_organizador = u.id_usuario
            WHERE v.id_viaje = %(id_viaje)s;
        """
        data = {'id_viaje': id_viaje}
        results = connectToMySQL(DATABASE).query_db(query, data)
        return cls(results[0]) if results else None

    @classmethod
    def eliminar(cls, id_viaje):
        query1 = "DELETE FROM participantes_viaje WHERE id_viaje = %(id_viaje)s;"
        query2 = "DELETE FROM viajes WHERE id_evento = %(id_viaje)s;"
        data = {'id_viaje': id_viaje}
        connectToMySQL(DATABASE).query_db(query1, data)
        connectToMySQL(DATABASE).query_db(query2, data)
        return True

    @classmethod
    def obtener_por_organizador(cls, id_organizador):
        query = """
            SELECT v.*, u.nombre as organizador 
            FROM viajes v
            JOIN usuarios u ON v.id_organizador = u.id_usuario
            WHERE v.id_organizador = %(id_organizador)s
            ORDER BY v.fecha_inicio;
        """
        data = {'id_organizador': id_organizador}
        results = connectToMySQL(DATABASE).query_db(query, data)
        viajes = []
        if results:
            for row in results:
                viajes.append(cls(row))
        return viajes

    # Método para validar los datos del evento
    @staticmethod
    def validar_viaje(data):
        errores = []
        
        # Validar que los campos no estén vacíos
        if not data['destino']:
            errores.append("El destino es obligatorio")
        
        if not data['fecha_inicio']:
            errores.append("La fecha de inicio es obligatoria")
            
        if not data['fecha_fin']:
            errores.append("La fecha de fin es obligatoria")

        # Validar fechas
        fecha_inicio = datetime.strptime(data['fecha_inicio'], '%Y-%m-%dT%H:%M')
        if fecha_inicio <= datetime.now():
            errores.append("La fecha de inicio debe ser una fecha futura")

        fecha_fin = datetime.strptime(data['fecha_fin'], '%Y-%m-%dT%H:%M')
        if fecha_fin <= datetime.now():
            errores.append("La fecha de fin debe ser una fecha futura")

        return errores
    