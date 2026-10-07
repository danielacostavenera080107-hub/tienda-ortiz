import urllib.parse
import pandas as pd
import streamlit as st

# 1. Configuración de la página (EVITA EL ERROR DE TRADUCCIÓN)
st.set_page_config(
    page_title="Mi Tienda - Pedidos", page_icon="🛒", layout="centered"
)

# Inyecta etiqueta HTML para prevenir que Google Translate rompa la app
st.markdown(
    """
    <script>
        document.documentElement.setAttribute('lang', 'es');
        document.documentElement.classList.add('notranslate');
    </script>
    """,
    unsafe_allow_html=True,
)

# 2. Configura tu número de WhatsApp real (Código de país + número sin '+' ni espacios)
# Ejemplo para Colombia: "573001234567"
NUMERO_WHATSAPP = "573243882384"  # ← CAMBIA ESTE NÚMERO POR EL TUYO

# Inicializar carrito
if "carrito" not in st.session_state:
    st.session_state.carrito = {}

# Catálogo de productos de ejemplo
PRODUCTOS_DEMO = [
    {
        "id": 1,
        "nombre": "Arroz Roa 1kg",
        "precio": 4000,
        "categoria": "Abarrotes",
    },
    {
        "id": 2,
        "nombre": "Aceite Vegetal 900ml",
        "precio": 12000,
        "categoria": "Abarrotes",
    },
    {
        "id": 3,
        "nombre": "Leche Entera 1L",
        "precio": 4200,
        "categoria": "Lácteos",
    },
    {
        "id": 4,
        "nombre": "Dolex 500mg (Caja x10)",
        "precio": 6500,
        "categoria": "Medicamentos",
    },
    {
        "id": 5,
        "nombre": "Jabón de Baño 120g",
        "precio": 3500,
        "categoria": "Aseo",
    },
]

st.title("🛒 Tienda Ortiz")
st.subheader("Realiza tu pedido y te lo alistamos para entrega")

# Selector de Categorías
categorias = ["Todas"] + list(set(p["categoria"] for p in PRODUCTOS_DEMO))
cat_seleccionada = st.selectbox("Filtrar por categoría:", categorias)

st.write("---")

# Mostrar lista de productos
for p in PRODUCTOS_DEMO:
    if cat_seleccionada == "Todas" or p["categoria"] == cat_seleccionada:
        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown(f"**{p['nombre']}**\n\n${p['precio']:,}")
        with col2:
            cant = st.number_input(
                "Cantidad",
                min_value=0,
                max_value=30,
                value=st.session_state.carrito.get(p["id"], 0),
                key=f"prod_{p['id']}",
            )
            st.session_state.carrito[p["id"]] = cant

st.write("---")
st.header("📋 Resumen de tu Pedido")

items_pedido = []
total = 0

for p in PRODUCTOS_DEMO:
    cant = st.session_state.carrito.get(p["id"], 0)
    if cant > 0:
        subtotal = cant * p["precio"]
        total += subtotal
        items_pedido.append(f"• {cant}x {p['nombre']} — ${subtotal:,}")

if items_pedido:
    for item in items_pedido:
        st.write(item)
    st.markdown(f"### **Total: ${total:,}**")

    st.subheader("Datos para el despacho")
    nombre = st.text_input("Tu Nombre Completo *")
    direccion = st.text_input("Dirección de Entrega / Barrio *")
    metodo_pago = st.selectbox(
        "Método de Pago *", ["Efectivo", "Nequi", "Daviplata", "Datafono/Tarjeta"]
    )
    notas = st.text_area("Notas o indicaciones adicionales (opcional)")

    if st.button("🚀 Confirmar y Enviar Pedido por WhatsApp"):
        if not nombre or not direccion:
            st.error(
                "Por favor completa tu nombre y dirección antes de enviar."
            )
        else:
            # Texto formateado para WhatsApp
            mensaje = f"🛒 *NUEVO PEDIDO - TIENDA ORTIZ*\n\n"
            mensaje += f"👤 *Cliente:* {nombre}\n"
            mensaje += f"📍 *Dirección:* {direccion}\n"
            mensaje += f"💳 *Pago:* {metodo_pago}\n"
            if notas:
                mensaje += f"📝 *Notas:* {notas}\n"
            mensaje += f"\n───────────────\n"
            mensaje += "\n".join(items_pedido)
            mensaje += f"\n───────────────\n"
            mensaje += f"💰 *TOTAL A COBRAR: ${total:,}*"

            mensaje_url = urllib.parse.quote(mensaje)
            link_wa = f"https://wa.me/{NUMERO_WHATSAPP}?text={mensaje_url}"

            st.success("¡Pedido generado con éxito!")
            st.link_button("📱 Abrir WhatsApp para enviar", link_wa)
else:
    st.info("Selecciona al menos un producto para realizar tu pedido.")
