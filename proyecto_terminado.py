import streamlit as st
import random
import re

st.set_page_config(page_title="Captcha Vial y Urbano", layout="centered")

TAMANO_IMAGENES = 160

BANCO_CAPTCHA = {
    "Semáforos ": [
        {"item": "imagenes/semaforo1.jpg", "es_correcto": True},
        {"item": "imagenes/semaforo2.jpg", "es_correcto": True},
        {"item": "imagenes/paso1.jpg", "es_correcto": False}, 
        {"item": "imagenes/hidrante1.jpg", "es_correcto": False}, 
        {"item": "imagenes/puente1.jpg", "es_correcto": False}, 
        {"item": "imagenes/montana1.jpg", "es_correcto": False}  
    ],
    "Pasos peatonales ": [
        {"item": "imagenes/paso1.jpg", "es_correcto": True},
        {"item": "imagenes/paso2.jpg", "es_correcto": True},
        {"item": "imagenes/semaforo1.jpg", "es_correcto": False}, 
        {"item": "imagenes/hidrante2.jpg", "es_correcto": False}, 
        {"item": "imagenes/chimenea1.jpg", "es_correcto": False}, 
        {"item": "imagenes/palmera1.jpg", "es_correcto": False}  
    ],
    "Bocas de incendio ": [
        {"item": "imagenes/hidrante1.jpg", "es_correcto": True},
        {"item": "imagenes/hidrante2.jpg", "es_correcto": True},
        {"item": "imagenes/puente2.jpg", "es_correcto": False}, 
        {"item": "imagenes/chimenea2.jpg", "es_correcto": False}, 
        {"item": "imagenes/palmera2.jpg", "es_correcto": False}, 
        {"item": "imagenes/montana2.jpg", "es_correcto": False}  
    ],
    "Puentes ": [
        {"item": "imagenes/puente1.jpg", "es_correcto": True},
        {"item": "imagenes/puente2.jpg", "es_correcto": True},
        {"item": "imagenes/montana1.jpg", "es_correcto": False}, 
        {"item": "imagenes/paso2.jpg", "es_correcto": False}, 
        {"item": "imagenes/semaforo2.jpg", "es_correcto": False}, 
        {"item": "imagenes/hidrante1.jpg", "es_correcto": False}  
    ],
    "Chimeneas ": [
        {"item": "imagenes/chimenea1.jpg", "es_correcto": True},
        {"item": "imagenes/chimenea2.jpg", "es_correcto": True},
        {"item": "imagenes/palmera1.jpg", "es_correcto": False}, 
        {"item": "imagenes/semaforo1.jpg", "es_correcto": False}, 
        {"item": "imagenes/paso1.jpg", "es_correcto": False}, 
        {"item": "imagenes/puente1.jpg", "es_correcto": False}  
    ],
    "Montañas ": [
        {"item": "imagenes/montana1.jpg", "es_correcto": True},
        {"item": "imagenes/montana2.jpg", "es_correcto": True},
        {"item": "imagenes/chimenea1.jpg", "es_correcto": False}, 
        {"item": "imagenes/hidrante2.jpg", "es_correcto": False}, 
        {"item": "imagenes/semaforo2.jpg", "es_correcto": False}, 
        {"item": "imagenes/puente2.jpg", "es_correcto": False}  
    ],
    "Palmeras ": [
        {"item": "imagenes/palmera1.jpg", "es_correcto": True},
        {"item": "imagenes/palmera2.jpg", "es_correcto": True},
        {"item": "imagenes/montana2.jpg", "es_correcto": False}, 
        {"item": "imagenes/chimenea2.jpg", "es_correcto": False}, 
        {"item": "imagenes/puente1.jpg", "es_correcto": False}, 
        {"item": "imagenes/hidrante1.jpg", "es_correcto": False}  
    ]
}

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "captcha_superado" not in st.session_state:
    st.session_state.captcha_superado = False
if "mostrar_error" not in st.session_state:
    st.session_state.mostrar_error = False
if "intentos_captcha" not in st.session_state:
    st.session_state.intentos_captcha = 0
if "fallos_acumulados" not in st.session_state:
    st.session_state.fallos_acumulados = 0
if "bloqueado" not in st.session_state:
    st.session_state.bloqueado = False

if "input_usuario" not in st.session_state:
    st.session_state.input_usuario = ""
if "input_contrasena" not in st.session_state:
    st.session_state.input_contrasena = ""

if "codigo_verificacion" not in st.session_state:
    st.session_state.codigo_verificacion = None
if "mostrar_apartado_codigo" not in st.session_state:
    st.session_state.mostrar_apartado_codigo = False

if "usuarios_db" not in st.session_state:
    st.session_state.usuarios_db = {}

if "usuario_en_recuperacion" not in st.session_state:
    st.session_state.usuario_en_recuperacion = None

PROVINCIAS = {
    "01": "Azuay", "02": "Bolívar", "03": "Cañar", "04": "Carchi", "05": "Cotopaxi",
    "06": "Chimborazo", "07": "El Oro", "08": "Esmeraldas", "09": "Guayas", "10": "Imbabura",
    "11": "Loja", "12": "Los Ríos", "13": "Manabí", "14": "Morona Santiago", "15": "Napo",
    "16": "Pastaza", "17": "Pichincha", "18": "Tungurahua", "19": "Zamora Chinchipe",
    "20": "Galápagos", "21": "Sucumbíos", "22": "Orellana", "23": "Santo Domingo de los Tsáchilas",
    "24": "Santa Elena", "30": "Exterior"
}

def generar_nuevo_captcha():
    tema = random.choice(list(BANCO_CAPTCHA.keys()))
    st.session_state.tema_actual = tema
    st.session_state.opciones_actuales = random.sample(BANCO_CAPTCHA[tema], 6)
    st.session_state.respuestas_usuario = [False] * 6
    st.session_state.intentos_captcha += 1

if "tema_actual" not in st.session_state:
    generar_nuevo_captcha()

def es_nombre_valido(texto):
    if not texto:
        return True
    return bool(re.match("^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$", texto))

def validar_cedula_real(cedula):
    if not cedula.isdigit() or len(cedula) != 10:
        return False, "Debe contener exactamente 10 números."
    
    prov = cedula[0:2]
    if prov not in PROVINCIAS:
        return False, "Esa cédula es falsa (Código de provincia inválido)."
    
    if int(cedula[2]) >= 6:
        return False, "Esa cédula es falsa (Tercer dígito inválido para cédula ciudadana)."
    
    coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    suma = sum(int(cedula[i]) * coeficientes[i] - (9 if int(cedula[i]) * coeficientes[i] >= 10 else 0) for i in range(9))
    esperado = (10 - (suma % 10)) % 10
    
    if int(cedula[9]) == esperado:
        return True, PROVINCIAS[prov]
    return False, "Esa cédula es FALSA (El dígito verificador matemático no coincide)."

def verificar_politica_contrasena(password):
    if len(password) < 8: return False, "La contraseña debe tener mínimo 8 caracteres."
    if not any(c.isupper() for c in password): return False, "Debe contener al menos una letra MAYÚSCULA."
    if not any(c.islower() for c in password): return False, "Debe contener al menos una letra minúscula."
    if not any(c.isdigit() for c in password): return False, "Debe incluir al menos un número."
    if not any(c in r"!@#$%^&*()_+-=[]{}|;':\",.<>?/~`" for c in password): return False, "Debe incluir al menos un carácter especial (Ej: @, #, $, !)."
    return True, ""

@st.dialog("Acceso Denegado")
def mostrar_error_bloqueo():
    st.error("❌ Error: Usted no pudo loguearse.")
    st.write("Ha agotado el número máximo de intentos permitidos para el captcha.")
    if st.button("Aceptar", type="primary"):
        st.session_state.clear()
        st.rerun()

@st.dialog("Verificación de Seguridad")
def abrir_ventana_captcha():
    st.markdown(f"### Selecciona todas las casillas que contengan: **{st.session_state.tema_actual}**")
    
    columnas = st.columns(3) + st.columns(3)
    for idx, col in enumerate(columnas):
        with col:
            st.image(st.session_state.opciones_actuales[idx]["item"], width=TAMANO_IMAGENES)
            key_checkbox = f"cb_{st.session_state.tema_actual}_{st.session_state.intentos_captcha}_{idx}"
            st.session_state.respuestas_usuario[idx] = st.checkbox(
                f"Imagen {idx+1}", 
                value=False, 
                key=key_checkbox
            )
            
    st.markdown("---")
    if st.button("Aceptar", type="primary"):
        es_valido = all(st.session_state.respuestas_usuario[i] == opc["es_correcto"] for i, opc in enumerate(st.session_state.opciones_actuales))
        
        if es_valido:
            st.session_state.captcha_superado = True
            st.session_state.mostrar_error = False
            st.rerun()
        else:
            st.session_state.fallos_acumulados += 1
            if st.session_state.fallos_acumulados >= 3:
                st.session_state.bloqueado = True
                st.rerun()
            else:
                st.session_state.captcha_superado = False
                st.session_state.mostrar_error = True
                generar_nuevo_captcha()
                st.rerun()

@st.dialog("Recuperar Contraseña")
def recuperar_contrasena():
    if not st.session_state.mostrar_apartado_codigo:
        st.write("Introduce tu nombre de usuario para enviarte las instrucciones de recuperación.")
        user_recup = st.text_input("Nombre de Usuario", key="user_recup_input").strip()
        
        usuario_valido = es_nombre_valido(user_recup)
        if not usuario_valido:
            st.error("⚠️ El nombre de usuario no debe contener números ni caracteres especiales.")
        
        if st.button("Enviar código de verificación", type="primary", disabled=not usuario_valido):
            if user_recup in st.session_state.usuarios_db:
                st.session_state.usuario_en_recuperacion = user_recup
                st.session_state.codigo_verificacion = str(random.randint(100000, 999999))
                
                print("\n" + "="*50)
                print(f"🔑 [SISTEMA] Código de recuperación para {user_recup}: {st.session_state.codigo_verificacion}")
                print("="*50 + "\n")
                
                st.session_state.mostrar_apartado_codigo = True
                st.rerun()
                
            elif not user_recup:
                st.warning("Por favor, introduce un nombre de usuario.")
            else:
                st.error("El usuario ingresado no existe en el sistema.")

    else:
        st.write("### 📩 Verificación de Seguridad")
        st.info("Se ha enviado un código de verificación de forma simulada. Por favor, revise la terminal de su entorno de desarrollo e ingréselo aquí:")
        
        codigo_usuario = st.text_input("Ingrese el código enviado a su correo", key="codigo_usuario_input", placeholder="Ej: 123456")
        
        col_validar, col_cancelar = st.columns(2)
        
        with col_validar:
            if st.button("Aceptar / Validar Código", type="primary", use_container_width=True):
                if codigo_usuario == st.session_state.codigo_verificacion:
                    user_actual = st.session_state.usuario_en_recuperacion
                    pass_recuperada = st.session_state.usuarios_db[user_actual]["password"]
                    
                    st.success("✅ ¡Código verificado correctamente!")
                    st.markdown(f"### Tu contraseña es: **{pass_recuperada}**")
                    
                    if st.button("Cerrar Ventana", use_container_width=True):
                        st.session_state.mostrar_apartado_codigo = False
                        st.session_state.codigo_verificacion = None
                        st.session_state.usuario_en_recuperacion = None
                        st.rerun()
                else:
                    st.error("❌ El código ingresado es incorrecto. Verifique la terminal e intente de nuevo.")
                    
        with col_cancelar:
            if st.button("Volver a intentar", use_container_width=True):
                st.session_state.mostrar_apartado_codigo = False
                st.session_state.codigo_verificacion = None
                st.session_state.usuario_en_recuperacion = None
                st.rerun()

if st.session_state.bloqueado:
    mostrar_error_bloqueo()

pestana_login, pestana_registro = st.tabs(["Iniciar Sesión", "Registro de Usuario"])

with pestana_login:
    st.title("Acceso Seguro")

    usuario = st.text_input("Nombre de Usuario", value=st.session_state.input_usuario)
    contrasena = st.text_input("Contraseña", type="password", value=st.session_state.input_contrasena)

    login_usuario_valido = es_nombre_valido(usuario)
    if not login_usuario_valido:
        st.error("⚠️ El nombre de usuario no puede contener números ni caracteres especiales.")

    if st.session_state.mostrar_error:
        verificar = st.checkbox("No soy un robot", value=False, key="robot_check_error")
    else:
        verificar = st.checkbox("No soy un robot", value=st.session_state.captcha_superado, disabled=st.session_state.captcha_superado, key="robot_check_normal")

    if verificar and not st.session_state.captcha_superado and not st.session_state.bloqueado:
        abrir_ventana_captcha()

    if st.session_state.mostrar_error and not st.session_state.bloqueado:
        st.error(f"❌ Fallaste el captcha (Intento {st.session_state.fallos_acumulados} de 3). Las imágenes cambiaron, vuelve a marcar la casilla.")

    st.markdown("---")

    col_ingresar, col_olvido = st.columns([1, 1])

    with col_ingresar:
        if st.button("Ingresar al Sistema", type="primary", use_container_width=True, disabled=not login_usuario_valido):
            if not usuario or not contrasena:
                st.warning("Por favor, ingresa tus credenciales.")
            elif usuario not in st.session_state.usuarios_db or st.session_state.usuarios_db[usuario]["password"] != contrasena:
                st.error("Credenciales incorrectas.")
            elif not st.session_state.captcha_superado:
                st.error("Por favor, supera la verificación humana obligatoriamente.")
            else:
                st.session_state.autenticado = True
                st.success(f"🎉 ¡Bienvenido, {usuario}! Has ingresado correctamente al sistema desde la provincia de {st.session_state.usuarios_db[usuario]['provincia']}.")
                st.switch_page("pages/pagina_web.py")

    with col_olvido:
        if st.button("¿Olvidaste tu contraseña?", use_container_width=True):
            recuperar_contrasena()

with pestana_registro:
    st.subheader("Formulario de Alta de Usuario")
    
    input_nombre = st.text_input("Nombre", key="reg_nombre").strip()
    if input_nombre and not re.match(r"^[A-Za-zÁéíóúáéíóúÑñ ]+$", input_nombre):
        st.error("Alerta! El campo 'Nombre' no admite números ni caracteres especiales.")
        input_nombre = ""
        
    input_apellido = st.text_input("Apellido", key="reg_apellido").strip()
    if input_apellido and not re.match(r"^[A-Za-zÁéíóúáéíóúÑñ ]+$", input_apellido):
        st.error("Alerta! El campo 'Apellido' no admite números ni caracteres especiales.")
        input_apellido = ""

    input_correo = st.text_input("Correo Institucional/Personal", key="reg_correo").strip()
    input_cedula = st.text_input("Cédula de Identidad de Ecuador (10 dígitos)", max_chars=10, key="reg_cedula").strip()
    input_pass = st.text_input("Contraseña de Alta Seguridad", type="password", help="Mínimo 8 caracteres, 1 Mayúscula, 1 Número y 1 Carácter Especial", key="reg_pass")
    
    st.markdown("---")

    if st.button("Crear y Validar Cuenta", type="secondary", use_container_width=True):
        if not all([input_nombre, input_apellido, input_correo, input_cedula, input_pass]):
            st.error("No se puede procesar el registro. Existen campos vacíos o con datos prohibidos.")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", input_correo):
            st.error("El correo electrónico ingresado no tiene una estructura válida.")
        else:
            cedula_ok, prov_detectada = validar_cedula_real(input_cedula)
            if not cedula_ok:
                st.error(f"Cédula Inválida: {prov_detectada}")
            else:
                pass_ok, msg_error_pass = verificar_politica_contrasena(input_pass)
                if not pass_ok:
                    st.error(f"Contraseña Débil: {msg_error_pass}")
                elif input_nombre in st.session_state.usuarios_db:
                    st.error("Este nombre de usuario ya se encuentra registrado.")
                else:
                    st.session_state.usuarios_db[input_nombre] = {
                        "nombre": input_nombre, 
                        "apellido": input_apellido, 
                        "correo": input_correo,
                        "cedula": input_cedula,
                        "provincia": prov_detectada, 
                        "password": input_pass
                    }
                    st.success(f"¡Usuario **{input_nombre}** verificado e inscrito correctamente! Provincia: {prov_detectada}.")