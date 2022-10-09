from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models.receta import Receta
from flask_app.models.usuario import Usuario

#página para crear una nueva receta
@app.route('/receta/nueva')
def nueva_receta():
    if 'user_id' not in session:
        return redirect('/logout')

    data = {
        "id":session['user_id']
    }

    return render_template('nueva_receta.html',user=Usuario.get_by_id(data))

#ruta para enviar a formulario y crear una receta nueva
@app.route('/receta_crear', methods=['POST'])
def crear_receta():

    if 'user_id' not in session:
        return redirect('/logout')

    if not Receta.validar_receta(request.form):
        return redirect('/receta/nueva')

    data = {
        "titulo_receta": request.form['titulo_receta'],
        "descripcion": request.form['descripcion'],
        "instrucciones": request.form['instrucciones'],
        "fecha": request.form['fecha'],
        "under30": request.form['under30'],
        "usuario_id": session["user_id"]
    }

    Receta.save_receta(data)
    return redirect('/dashboard')

@app.route('/receta/<int:id>')
def mostrar_receta(id):
    if 'user_id' not in session:
        return redirect('/logout')

    data = {
        "id":id
    }

    data_usuario = {
        "id":session['user_id']
    }
    return render_template("mostrar.html",receta=Receta.obtener_una_receta(data),usuario=Usuario.get_by_id(data_usuario))

@app.route('/receta/editar/<int:id>')
def editar_receta(id):

    if 'user_id' not in session:
        return redirect('/logout')

    data = {
        "id":id
    }

    return render_template("editar.html", una_receta=Receta.obtener_una_receta(data))

@app.route('/receta/actualizar', methods=['POST'])
def actualizar_receta():

    if 'user_id' not in session:
        return redirect('/logout')

    if not Receta.validar_receta(request.form):
        return redirect('/receta/nueva')


    Receta.update(request.form)
    return redirect('/dashboard')


@app.route('/receta/eliminar/<int:id>')
def borrar_receta(id):
    
    data ={ 
        "id":id
    }
    Receta.destroy(data)
    return redirect('/dashboard')