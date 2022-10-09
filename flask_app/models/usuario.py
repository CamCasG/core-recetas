from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.receta import Receta
import re
from datetime import date, datetime    
from flask_bcrypt import Bcrypt   


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
REGEX_PASSWORD = re.compile(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])[a-zA-Z\d]{7,16}$")  #contraseña debe contener mayúsculas, minúsculas y números, y un mínimo de 7 caracteres
NAME_REGEX = re.compile(r'^([A-Za-z\D]){3,}$')   #solo debe contener letras y un mínimo de 3 caracteres

class Usuario:
    def __init__(self,data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']
        self.nacimiento = data['nacimiento']
        self.genero = data['genero']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recetas_favoritas = []


    @classmethod
    def agregar_favorito(cls,data):
        #agregar a favoritos
        query = "INSERT INTO recetas_favoritas (nombre_id, receta_id) VALUES (%(nombre_id)s,%(receta_id)s);"
        resultado = connectToMySQL('esquema_recetas').query_db(query,data)
        print(resultado)
        return resultado

    @classmethod
    def save_user(cls,data):
        query = "INSERT INTO usuarios (nombre, apellido, email, password, nacimiento, genero) VALUES (%(nombre)s,%(apellido)s,%(email)s,%(password)s,%(nacimiento)s,%(genero)s);"
        resultado = connectToMySQL('esquema_recetas').query_db(query,data)
        print(resultado)
        return resultado

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        result = connectToMySQL('esquema_recetas').query_db(query,data)
        # no se encontró un usuario coincidente
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        results = connectToMySQL('esquema_recetas').query_db(query,data)
        return cls(results[0])

    @staticmethod
    def validar_usuario(usuario):
        today = date.today() 
        is_valid = True
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        resultado = connectToMySQL('esquema_recetas').query_db(query,usuario)
        hoy = today.strftime("%Y-%m-%d")
        edad = datetime.strptime(hoy,'%Y-%m-%d').date()
        print(hoy)
        nacimiento = usuario['nacimiento']
        cumpleanos = datetime.strptime(nacimiento,'%Y-%m-%d').date()
        print(cumpleanos)

        if len(resultado) >= 1:
            is_valid = False
            flash("Ya te has registrado con este correo antes.", "registro")
        if not NAME_REGEX.match(usuario['nombre']):
            is_valid = False
            flash("El nombre debe tener por lo menos 3 caracteres y no contener números","registro")
        if not NAME_REGEX.match(usuario['apellido']):
            is_valid = False
            flash("El apellido debe tener por lo menos 3 caracteres y no contener números","registro")
        if not EMAIL_REGEX.match(usuario['email']):
            is_valid = False
            flash("Correo electrónico inválido, volver a intentar.","registro")
        if not REGEX_PASSWORD.match(usuario['password']):
            is_valid = False
            flash("Tu contraseña debe contener mayúsculas, minúsculas, números y un mínimo de 7 caracteres","registro")
        if usuario['password'] != usuario['confirmar']:
            is_valid = False
            flash("¡Las contraseñas no coinciden!","registro")
        if edad.year - cumpleanos.year - ((cumpleanos.month, edad.day) <  (cumpleanos.month, edad.day)) < 12:
            is_valid = False
            flash("¡Alto ahí! No tienes edad suficiente para registrarte a nuesta página.", "registro")

        return is_valid