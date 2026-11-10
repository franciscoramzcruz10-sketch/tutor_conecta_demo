from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'cambia-esta-clave-secreta'

# Primer número de control permitido (de este en adelante)
CONTROL_INICIAL = 25415082210054
MENSAJE_ERROR = 'Número de control no válido. Debe tener 14 dígitos y ser 25415082210054 o mayor.'

# Páginas que se pueden abrir sin iniciar sesión
PAGINAS_PUBLICAS = ('inicio', 'registro', 'inicio_sesion', 'cerrar_sesion', 'static')


def control_valido(numero):
    return numero.isdigit() and len(numero) == 14 and int(numero) >= CONTROL_INICIAL


# Se ejecuta antes de cada página: si no hay sesión, manda al login
@app.before_request
def revisar_sesion():
    if request.endpoint and request.endpoint not in PAGINAS_PUBLICAS and 'numero_control' not in session:
        return redirect(url_for('inicio_sesion'))


# Pantalla de bienvenida
@app.route('/')
def inicio():
    return render_template('index.html')


# Crear cuenta con número de control
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        numero = request.form.get('numero_control', '').strip()
        if control_valido(numero):
            session['numero_control'] = numero
            return redirect(url_for('panel_principal'))
        return render_template('registro.html', error=MENSAJE_ERROR)
    return render_template('registro.html')


# Iniciar sesión con número de control
@app.route('/login', methods=['GET', 'POST'])
def inicio_sesion():
    if request.method == 'POST':
        numero = request.form.get('numero_control', '').strip()
        if control_valido(numero):
            session['numero_control'] = numero
            return redirect(url_for('panel_principal'))
        return render_template('login.html', error=MENSAJE_ERROR)
    return render_template('login.html')


@app.route('/salir')
def cerrar_sesion():
    session.clear()
    return redirect(url_for('inicio_sesion'))


# Panel principal con las opciones
@app.route('/panel')
def panel_principal():
    return render_template('panel.html', numero_control=session['numero_control'])


@app.route('/alumnos')
def registro_alumnos():
    return render_template('alumnos.html')


@app.route('/calificaciones')
def calificaciones():
    return render_template('calificaciones.html')


@app.route('/asistencias')
def asistencias():
    return render_template('asistencias.html')


@app.route('/inasistencias')
def inasistencias():
    return render_template('inasistencias.html')


@app.route('/reportes')
def reportes():
    return render_template('reportes.html')


@app.route('/quejas')
def quejas():
    return render_template('quejas.html')


if __name__ == '__main__':
    app.run(debug=True)