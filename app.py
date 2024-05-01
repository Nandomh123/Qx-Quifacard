import os
from flask import Flask
from flask import render_template, request, redirect, session, url_for
from flask import send_from_directory
from sqlalchemy import create_engine
import pandas as pd
#import pymysql
import numpy as np
import datetime
from flask_mysqldb import MySQL
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sitio'
mysql = MySQL(app)


#--------------------------------------------
# Link a las pestañas
#--------------------------------------------

# index
@app.route('/')
def inicio():
    return render_template( 'sitio/index.html')

# productos
@app.route('/productos')
def productos():
    return render_template( 'sitio/productos.html')

# nosotros
@app.route('/nosotros')
def nosotros():
    return render_template( 'sitio/nosotros.html')

# login-registro
@app.route('/Login-Registro')
def login_registro():
    return render_template( 'sitio/login_registro.html')

# session
@app.route('/sesion')
def sesion():
    return render_template( 'sitio/sesion.html')

@app.route('/sitio/login_registro/guardar', methods = ['POST'])
def submit_registro():
    # Recuperar datos del formulario
    _nombre_completo = request.form['nombre_completo']
    _correo_electronico= request.form['correo']
    _usuario = request.form['usuario']
    _contrasenia = request.form['contrasena']
    # Ejecutar consulta SQL para insertar datos en la base de datos
    conn = mysql.connection
    cursor = conn.cursor()
    sql = "INSERT INTO `registro`(ID,NOMBRE_COMPLETO, CORREO_ELECTRONICO, USUARIO, CONTRASENIA) VALUES (null, %s, %s, %s, %s )"
    cursor.execute(sql, ( _nombre_completo,_correo_electronico, _usuario, _contrasenia  ))
    conn.commit()
    return redirect('/Login-Registro')

# Funcion Login Final
@app.route('/sitio/acceso-login', methods = ['GET','POST'])
def login():
    if request.method == 'POST' and 'ingrese_correo' in request.form and 'ingrese_contraseña':
        correo_ = request.form['ingrese_correo']
        password_ = request.form['ingrese_contraseña']
        # Ejecuta la instrucción para ver si existe el correo
        conn = mysql.connection
        cursor = conn.cursor()
        sql = "SELECT * FROM `registro` WHERE CORREO_ELECTRONICO = %s and CONTRASENIA = %s"
        cursor.execute(sql, ( correo_, password_, ))
        account = cursor.fetchone()
        cursor.close()
        if account:
            session['nombre_completo'] = account[1]
            session['correo'] = correo_
            session['logueado'] = True
            return redirect('/sesion')
        else:
            return render_template('/sitio/login_registro.html', mensaje = "Usuario o contraseña incorrecta") 
            
        
@app.route('/logout')
def logout():
    session.clear() 
    return redirect('/Login-Registro')

if __name__ == "__main__":
    app.secret_key = "Nandomh123"
    app.run( debug = True )

