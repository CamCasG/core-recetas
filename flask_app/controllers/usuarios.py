from flask_app.models.usuario import Usuario
from flask_app.models.receta import Receta
from flask import redirect, render_template, request, session, flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)  # estamos creando un objeto llamado bcrypt,
# que se realiza invocando la función Bcrypt con nuestra aplicación como argumento
from flask import flash


@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/registrar', methods=['POST'])
def registro():
    is_valid = Usuario.validar_usuario(request.form)
    # crear el hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    # poner pw_hash en el diccionario de datos
    if not is_valid:
        return redirect("/")
    data = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "email": request.form['email'],
        "password" : pw_hash,
        "nacimiento": request.form['nacimiento'],
        "genero": request.form['genero']
    }

    # llama al @classmethod de guardado en Usuario
    user_id = Usuario.save_user(data)
    # almacenar id de usuario en la sesión
    session['user_id'] = user_id
    return redirect("/dashboard")

@app.route('/login', methods=['POST'])
def login():
    # ver si el nombre de usuario proporcionado existe en la base de datos
    data = { "email" : request.form["email"] }
    user_in_db = Usuario.get_by_email(data)
    # usuario no está registrado en la base de datos
    if not user_in_db:
        flash("Correo inválido", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # si obtenemos False después de verificar la contraseña
        flash("Contraseña inválida", "login")
        return redirect('/')
    # si las contraseñas coinciden, configuramos el user_id en sesión
    session['user_id'] = user_in_db.id
    #! ¡¡¡Nunca renderices en una post!!!
    return redirect("/dashboard")

@app.route('/dashboard')
def resultado():
    #si el usuario guardado en user_id no se encuentra en session, redigirá a logout y se devolverá a la página de inicio de sesión y registro
    if 'user_id' not in session:
        return redirect('/logout')

    data ={
        'id': session['user_id']
    }


    return render_template("principal.html", usuario=Usuario.get_by_id(data), todas_las_recetas=Receta.obtener_recetas(data), una_receta=Receta.obtener_una_receta(data))


@app.route('/receta/fav', methods=['POST'])
def agregar_a_favoritos():

    if 'user_id' not in session:
        return redirect('/logout')

    data = {

        "nombre_id": session['user_id'],
        "receta_id": request.form['receta_id']

    }

    
    Usuario.agregar_favorito(data)
    print(Usuario.agregar_favorito(data))
    return redirect('/dashboard')


#ruta para cerrar sesión y volver a la página de inicio.
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')