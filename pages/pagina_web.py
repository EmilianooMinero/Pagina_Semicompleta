import streamlit as st

if "autenticado" not in st.session_state or not st.session_state.autenticado:
    st.error("🚫 Acceso Denegado. Por favor, inicia sesión primero en la página principal.")
    if st.button("Ir al Inicio de Sesión"):
        st.switch_page("proyecto_terminado.py")
    st.stop()

st.set_page_config(page_title="Ecomoda Calzado Premium", layout="wide", initial_sidebar_state="expanded")

if "carrito" not in st.session_state:
    st.session_state.carrito = []
if "vista" not in st.session_state:
    st.session_state.vista = "catalogo"
if "producto_seleccionado" not in st.session_state:
    st.session_state.producto_seleccionado = None

CATALOGO = [
    {
        "id": 1,
        "nombre": "Nike Air Max 90 Ultra",
        "marca": "Nike",
        "estado": "Segunda Mano",
        "calidad": "Excelente (9/10)",
        "precio": 45.00,
        "descripcion": "Clásicos Air Max con un porcentaje mínimo de uso. Conservan la amortiguación de aire intacta, suelas con tracción completa y un lavado higiénico profundo bajo estándares profesionales.",
        "imagen": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&q=80"
    },
    {
        "id": 2,
        "nombre": "Nike Dunk Low Retro Blue",
        "marca": "Nike",
        "estado": "Nuevo",
        "calidad": "A estrenar",
        "precio": 110.00,
        "descripcion": "Zapatillas icónicas de corte urbano completamente nuevas, directo en su caja original de fábrica. Estructura de cuero premium y balance perfecto de colores de temporada.",
        "imagen": "https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?w=600&q=80"
    },
    {
        "id": 3,
        "nombre": "Adidas Ultraboost 22 Core",
        "marca": "Adidas",
        "estado": "Segunda Mano",
        "calidad": "Muy Bueno (8/10)",
        "precio": 65.00,
        "descripcion": "Líderes en running urbano. El tejido superior Primeknit está intacto, libre de raspaduras. Presentan un leve desgaste estético en la plantilla interna trasera trasera.",
        "imagen": "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=600&q=80"
    },
    {
        "id": 4,
        "nombre": "Adidas Forum Low Classic",
        "marca": "Adidas",
        "estado": "Nuevo",
        "calidad": "A estrenar",
        "precio": 95.00,
        "descripcion": "El renacer de las canchas de baloncesto de 1984. Sistema de ajuste dual mediante cordones y correa de velcro superior. Cuero impecable de alta resistencia.",
        "imagen": "https://images.unsplash.com/photo-1518002171953-a080ee817e1f?w=600&q=80"
    },
    {
        "id": 5,
        "nombre": "Puma Classic Suede Heritage",
        "marca": "Puma",
        "estado": "Segunda Mano",
        "calidad": "Buen Estado (7/10)",
        "precio": 30.00,
        "descripcion": "Estilo clásico de gamuza retro. Tiene sutiles marcas naturales de uso exterior en los laterales que acentúan su look vintage sin comprometer costuras ni soporte.",
        "imagen": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=600&q=80"
    },
    {
        "id": 6,
        "nombre": "Puma Nitro High Runner",
        "marca": "Puma",
        "estado": "Nuevo",
        "calidad": "A estrenar",
        "precio": 85.00,
        "descripcion": "Calzado diseñado para alto rendimiento deportivo y amortiguación extrema usando espuma tecnológica Nitro inyectada. Incluye etiquetas y embalaje original.",
        "imagen": "https://images.unsplash.com/photo-1539185441755-769473a23570?w=600&q=80"
    }
]

def cambiar_vista(nueva_vista, producto=None):
    st.session_state.vista = nueva_vista
    st.session_state.producto_seleccionado = producto
    st.rerun()

def agregar_al_carrito(producto):
    st.session_state.carrito.append(producto)
    st.toast(f"🛒 **{producto['nombre']}** se añadió al carrito de compras.", icon="✅")

with st.sidebar:
    st.markdown("### 👤 Sesión Activa")
    if st.button("⬅️ Cerrar Sesión Segura", type="secondary", use_container_width=True):
        st.session_state.autenticado = False
        st.switch_page("proyecto_terminado.py")
        
    st.markdown("---")
    st.markdown("### 🎯 Panel de Filtros")
    filtro_estado = st.radio("Condición de las Zapatillas", ["Todos", "Nuevo", "Segunda Mano"], index=0)
    filtro_marca = st.selectbox("Filtrar por Diseñador / Marca", ["Todas", "Nike", "Adidas", "Puma"])
    
    st.markdown("---")
    st.markdown("### 👜 Carrito de Compras")
    if len(st.session_state.carrito) == 0:
        st.caption("No has añadido artículos.")
    else:
        st.success(f"Artículos listos: {len(st.session_state.carrito)}")
        total_acumulado = sum(p["precio"] for p in st.session_state.carrito)
        st.markdown(f"**Subtotal: ${total_acumulado:.2f}**")
        if st.button("💼 Procesar Carrito", type="primary", use_container_width=True):
            cambiar_vista("carrito")

if st.session_state.vista == "catalogo":
    st.title("👟 Ecomoda Calzado")
    st.markdown("---")
    
    productos_filtrados = CATALOGO
    if filtro_estado != "Todos":
        productos_filtrados = [p for p in productos_filtrados if p["estado"] == filtro_estado]
    if filtro_marca != "Todas":
        productos_filtrados = [p for p in productos_filtrados if p["marca"] == filtro_marca]
        
    if not productos_filtrados:
        st.warning("🔍 No encontramos calzado que coincida exactamente con los filtros seleccionados.")
    else:
        marcas_disponibles = sorted(list(set(p["marca"] for p in productos_filtrados)))
        
        for marca in marcas_disponibles:
            st.markdown(f"## 🏷️ Colección {marca}")
            productos_marca = [p for p in productos_filtrados if p["marca"] == marca]
            
            columnas = st.columns(3)
            for idx, prod in enumerate(productos_marca):
                with columnas[idx % 3]:
                    with st.container(border=True):
                        st.image(prod["imagen"], use_container_width=True)
                        
                        col_datos_izq, col_datos_der = st.columns([2, 1])
                        with col_datos_izq:
                            st.markdown(f"#### **{prod['nombre']}**")
                        with col_datos_der:
                            st.markdown(f"### `${prod['precio']:.2f}`")
                        
                        if prod["estado"] == "Nuevo":
                            st.markdown("🟢 **Condición:** `Nuevo / Original`")
                        else:
                            st.markdown(f"🔵 **Condición:** `Reusado - {prod['calidad']}`")
                            
                        st.write("")
                        if st.button("🔎 Inspeccionar Calzado", key=f"btn_ver_{prod['id']}", use_container_width=True, type="secondary"):
                            cambiar_vista("detalle", prod)
            st.markdown(" ")

elif st.session_state.vista == "detalle":
    prod = st.session_state.producto_seleccionado
    
    if st.button("⬅️ Regresar al Catálogo Principal", type="secondary"):
        cambiar_vista("catalogo")
        
    st.markdown("---")
    
    col_izq, col_der = st.columns([1.3, 1])
    
    with col_izq:
        st.image(prod["imagen"], use_container_width=True)
        
    with col_der:
        st.subheader(f"👟 {prod['marca']}")
        st.title(prod["nombre"])
        
        if prod["estado"] == "Nuevo":
            st.info("✨ **Garantía Ecomoda:** Este artículo es completamente nuevo, empaquetado de origen y nunca ha sido pisado.")
        else:
            st.warning(f"♻️ **Moda Sostenible:** Par de segunda mano verificado en calidad: **{prod['calidad']}**. Contribuyes a reducir la huella de carbono.")
            
        st.markdown("### 📋 Especificaciones y Detalles:")
        st.write(prod["descripcion"])
        st.markdown("---")
        
        col_pre, col_bot = st.columns([1, 1.5])
        with col_pre:
            st.markdown("Precio de Venta:")
            st.markdown(f"## **${prod['precio']:.2f}**")
        with col_bot:
            st.write("")
            if st.button("🛒 Añadir al Carrito", type="primary", use_container_width=True):
                agregar_al_carrito(prod)

elif st.session_state.vista == "carrito":
    st.title("💼 Desglose de tu Orden")
    if st.button("⬅️ Continuar Comprando", type="secondary"):
        cambiar_vista("catalogo")
        
    st.markdown("---")
    
    if len(st.session_state.carrito) == 0:
        st.info("Tu cesta de compras se encuentra vacía en este momento.")
    else:
        for idx, item in enumerate(st.session_state.carrito):
            with st.container(border=True):
                c1, c2, c3, c4 = st.columns([1, 3, 1.5, 1])
                with c1:
                    st.image(item["imagen"], width=80)
                with c2:
                    st.markdown(f"#### **{item['nombre']}**")
                    st.caption(f"Marca: {item['marca']} | Estado: {item['estado']}")
                with c3:
                    st.markdown(f"### `${item['precio']:.2f}`")
                with c4:
                    st.write("")
                    if st.button("Quitar", key=f"eliminar_{idx}", type="secondary", use_container_width=True):
                        st.session_state.carrito.pop(idx)
                        st.rerun()
                        
        total = sum(item["precio"] for item in st.session_state.carrito)
        
        st.markdown("---")
        c_tot1, c_tot2 = st.columns([4, 1])
        with c_tot1:
            st.markdown("### Total Neto de la Orden:")
        with c_tot2:
            st.markdown(f"## **${total:.2f}**")
            
        st.markdown("---")
        if st.button("🚀 Confirmar y Finalizar Pedido", type="primary", use_container_width=True):
            st.balloons()
            st.success("🎉 ¡Pedido registrado con éxito! Tu calzado está reservado. Gracias por apoyar el comercio circular.")
            st.session_state.carrito = []
            st.session_state.vista = "catalogo"