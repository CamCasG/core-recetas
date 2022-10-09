from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Receta:
    def __init__( self , data ):
        self.id = data['id']
        self.titulo_receta = data['titulo_receta']
        self.descripcion = data['descripcion']
        self.instrucciones = data['instrucciones']
        self.fecha = data['fecha']
        self.under30 = data['under30']
        self.usuario_id = data['usuario_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def obtener_una_receta(cls,data):
        query = "SELECT * FROM recetas WHERE id = %(id)s;"
        resultado = connectToMySQL('esquema_recetas').query_db(query,data)
        return cls(resultado[0])

    @classmethod
    def obtener_recetas(cls, data):
        query = "SELECT * FROM recetas JOIN usuarios WHERE recetas.usuario_id = usuarios.id;"
        resultado = connectToMySQL('esquema_recetas').query_db(query, data)
        return resultado

    @classmethod
    def save_receta(cls,data):
        query = "INSERT INTO recetas (titulo_receta, descripcion, instrucciones, fecha, under30, usuario_id) VALUES (%(titulo_receta)s,%(descripcion)s,%(instrucciones)s,%(fecha)s,%(under30)s,%(usuario_id)s);"
        resultado = connectToMySQL('esquema_recetas').query_db(query,data)
        print(resultado)
        return resultado

    @classmethod
    def update(cls,data):
        query = "UPDATE recetas SET titulo_receta=%(titulo_receta)s,descripcion=%(descripcion)s,instrucciones=%(instrucciones)s,fecha=%(fecha)s,under30=%(under30)s WHERE id = %(id)s;"
        return connectToMySQL('esquema_recetas').query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM recetas WHERE id = %(id)s;"
        return connectToMySQL('esquema_recetas').query_db(query,data)

    @staticmethod
    def validar_receta(receta):
        is_valid = True 

        if len(receta['titulo_receta']) < 1:
            flash("¡Este espacio no puede ir vacio!", 'receta')
            is_valid = False
        if len(receta['descripcion']) < 3:
            flash("¡Este espacio no puede ir vacio!", 'receta')
            is_valid = False
        if len(receta['instrucciones']) <  3:
            flash("¡Este espacio no puede ir vacio!", 'receta')
            is_valid = False
        if not(receta['fecha']):
            flash("Por favor, agregar la fecha la cual la receta fue creada", 'receta')
            is_valid = False
        if not(receta['under30']):
            flash("Por favor, escoger una opción", 'receta')
            is_valid = False
        return is_valid

    @classmethod
    def receta_especifica(cls,data):
        query = "SELECT * FROM recetas LEFT JOIN recetas_favoritas ON recetas.id = recetas_favoritas.receta_id LEFT JOIN usuarios ON usuarios.id = recetas_favoritas.nombre_id WHERE usuarios.id = %(id)s;"
        resultados = connectToMySQL('esquema_recetas').query_db(query,data)
        print(resultados)

        receta = cls(resultados[0])

        for row in resultados:

            receta_data = {

                "id": row['receta.id'],
                "titulo_receta": row['titulo_receta'],
                "descripcion": row['descripcion'],
                "instrucciones": row['instrucciones'],
                "fecha": row['fecha'],
                "under30": row['under30'],
                "usuario_id": row['usuario_id'],
                "created_at": row['receta.created_at'],
                "updated_at": row['receta.updated_at']
            }
            receta.recetas_favoritas.append(Receta(receta_data))
        return receta
