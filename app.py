from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import json
import os
import hashlib
import sqlite3
from pathlib import Path
from flask_session import Session

app = Flask(__name__)

# Configuración de la clave secreta para sesiones
app.secret_key = 'clave_secreta_segura'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Cargar datos de revistas
BASE_DIR = Path(__file__).parent
REVISTAS_JSON = BASE_DIR / 'datos' / 'json' / 'revistas.json'
SCIMAGOJR_JSON = BASE_DIR / 'datos' / 'json' / 'revistas_scimagojr.json'

def cargar_datos():
    with open(REVISTAS_JSON, 'r', encoding='utf-8') as f:
        revistas = json.load(f)

    if not SCIMAGOJR_JSON.exists():
        print(f"Advertencia: El archivo {SCIMAGOJR_JSON} no existe.")
        scimagojr = {}
    else:
        with open(SCIMAGOJR_JSON, 'r', encoding='utf-8') as f:
            try:
                scimagojr = json.load(f)
            except json.JSONDecodeError:
                print(f"Error: El archivo {SCIMAGOJR_JSON} no contiene un JSON válido.")
                scimagojr = {}

    return revistas, scimagojr

def init_user_db():
    db_path = os.path.join(BASE_DIR, 'instance', 'users.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def get_user_by_email(email):
    db_path = os.path.join(BASE_DIR, 'instance', 'users.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = c.fetchone()
    conn.close()
    return user

def create_user(name, email, password):
    db_path = os.path.join(BASE_DIR, 'instance', 'users.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        c.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Asegurarse de que la base de datos se inicialice al arrancar la aplicación
init_user_db()

# Rutas principales
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/areas')
def areas():
    revistas, _ = cargar_datos()
    # Obtener todas las áreas únicas
    areas = set()
    for info in revistas.values():
        areas.update(info['areas'])
    return render_template('areas.html', areas=sorted(areas))

# Ruta para la página de catálogos
@app.route('/catalogos')
def catalogos():
    revistas, _ = cargar_datos()
    # Obtener lista única de catálogos
    catalogos = set()
    for revista in revistas.values():
        catalogos.update(revista['catalogos'])
    return render_template('catalogos.html', catalogos=sorted(catalogos))

# Ruta para la página de explorar
@app.route('/explorar')
def explorar():
    return render_template('explorar.html')

# Eliminada la duplicación de la función buscar
# def buscar():
#     return render_template('buscar.html')

# Ruta para la página de búsqueda
@app.route('/buscar')
def buscar():
    query = request.args.get('q', '').lower()
    if not query:
        return render_template('buscar.html', revistas={})
    
    revistas, scimagojr = cargar_datos()
    # Buscar revistas que contengan la consulta
    resultados = {
        titulo: info for titulo, info in revistas.items()
        if query in titulo.lower()
    }
    return render_template('buscar.html', revistas=resultados, scimagojr=scimagojr, query=query)

# Ruta para la página de créditos
@app.route('/creditos')
def creditos():
    return render_template('creditos.html')

@app.route('/area/<area>')
def area_detalle(area):
    revistas, scimagojr = cargar_datos()
    # Filtrar revistas por área
    revistas_area = {
        titulo: info for titulo, info in revistas.items()
        if area in info['areas']
    }
    return render_template('area_detalle.html', area=area, revistas=revistas_area, scimagojr=scimagojr)

@app.route('/catalogo/<catalogo>')
def catalogo_detalle(catalogo):
    revistas, scimagojr = cargar_datos()
    # Filtrar revistas por catálogo
    revistas_catalogo = {
        titulo: info for titulo, info in revistas.items()
        if catalogo in info['catalogos']
    }
    return render_template('catalogo_detalle.html', catalogo=catalogo, revistas=revistas_catalogo, scimagojr=scimagojr)

@app.route('/explorar/<letra>')
def explorar_letra(letra):
    revistas, scimagojr = cargar_datos()
    # Filtrar revistas por letra inicial
    revistas_letra = {
        titulo: info for titulo, info in revistas.items()
        if titulo.lower().startswith(letra.lower())
    }
    return render_template('explorar_letra.html', letra=letra, revistas=revistas_letra, scimagojr=scimagojr)

@app.route('/revista/<titulo>')
def revista_detalle(titulo):
    revistas, scimagojr = cargar_datos()
    revista_info = revistas.get(titulo, {})
    scimagojr_info = scimagojr.get(titulo, {})
    return render_template('revista_detalle.html', 
                         titulo=titulo, 
                         revista=revista_info, 
                         scimagojr=scimagojr_info)

# Ruta para registrar usuarios
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not all([name, email, password, confirm_password]):
            return render_template('registro.html', error='Todos los campos son obligatorios.')

        if password != confirm_password:
            return render_template('registro.html', error='Las contraseñas no coinciden.')

        # Verificar si el usuario ya existe
        if get_user_by_email(email):
            return render_template('registro.html', error='El correo electrónico ya está registrado.')

        # Crear el usuario
        if create_user(name, email, password):
            # Iniciar sesión automáticamente
            session['user'] = {
                'name': name,
                'email': email
            }
            return redirect(url_for('index'))
        else:
            return render_template('registro.html', error='Error al crear el usuario. Intente nuevamente.')

    return render_template('registro.html')

# Ruta para iniciar sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        user = get_user_by_email(email)
        if user and user[3] == hashed_password:  # user[3] es la contraseña hasheada
            session['user'] = {
                'name': user[1],  # user[1] es el nombre
                'email': user[2]  # user[2] es el email
            }
            return redirect(url_for('index'))
        else:
            return render_template('inicio_sesion.html', error='Credenciales incorrectas')

    return render_template('inicio_sesion.html')

# Ruta para el perfil
@app.route('/perfil')
def perfil():
    if 'user' not in session:
        return redirect(url_for('login'))

    user = session['user']
    return render_template('perfil.html', user=user['name'])

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/add_to_profile', methods=['POST'])
def add_to_profile():
    if 'user' not in session:
        return jsonify({"success": False, "message": "Usuario no autenticado."}), 401

    data = request.get_json()
    title = data.get('title')

    if not title:
        return jsonify({"success": False, "message": "Título no proporcionado."}), 400

    # Simular agregar el artículo al perfil del usuario
    user = session['user']
    if 'saved_articles' not in user:
        user['saved_articles'] = []

    user['saved_articles'].append(title)
    session['user'] = user

    return jsonify({"success": True, "message": "Artículo agregado al perfil."})

@app.route('/newnoticias')
def newnoticias():
    return render_template('Newnoticias.html')

@app.route('/info1')
def info1():
    return render_template('info1.html')

@app.route('/info2')
def info2():
    return render_template('info2.html')

if __name__ == '__main__':
    app.run(debug=True)
