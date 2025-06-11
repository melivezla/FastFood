import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re  

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("No se encontró la clave API de Gemini. Usa un archivo .env.")
    st.stop()

# --- Validación de API Key ---
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")


# --- Configuración de la página ---
st.set_page_config(page_title="FastFood Chatbot", page_icon="🍟")

st.title("FastNutriBembos – Tu Guía Inteligente de Bembos")
st.write("Explora menús, recetas, combos y conoce sus calorías o valor nutricional.")

# --- Historial de conversación ---
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[
        {
        "role": "user",
        "parts": """
Actúa como un asistente experto de Bembos Perú. Tu tarea es ayudar a los usuarios a:

- Explorar el menú de Bembos (hamburguesas, combos, papas, postres y bebidas).
- Conocer ingredientes de los productos.
- Estimar las calorías o valor nutricional.
- Recomendar opciones según gustos o restricciones (ej. sin gluten, sin lactosa, vegetariano).
- Explicar promociones o diferencias entre combos si están disponibles.
- Ser amigable, conciso y confiable.

Responde de forma natural como si trabajaras en Bembos. Si no sabes una respuesta exacta, ofrece una sugerencia basada en tu conocimiento general.
"""
    }
    ])


for part in st.session_state.chat.history[1:]:
    role = part.role
    message = part.parts[0].text if hasattr(part.parts[0], "text") else str(part.parts[0])

    if role == "user":
        st.chat_message("user").markdown(message)
    else:
        st.chat_message("assistant").markdown(message)




user_input = st.chat_input("¿Qué te apetece comer hoy?")

if user_input:
    st.chat_message("user").markdown(user_input)

    # --- Validación de temas de Bembos ---
    temas_validos = [
        "bembos", "hamburguesa", "combo", "papas", "bebida", "postre",
        "menú", "ingredientes", "promoción", "calorías", "nutrición",
        "vegetariano", "sin gluten", "sin lactosa", "carne", "pollo"
    ]

    # --- Si no está relacionado con Bembos
    if not any(re.search(palabra, user_input, re.IGNORECASE) for palabra in temas_validos):
        respuesta = "Lo siento, no tengo información suficiente para ayudarte con esa solicitud. Solo puedo responder sobre productos y temas relacionados con **Bembos Perú**. 🍔"
        st.chat_message("assistant").markdown(respuesta)

    # --- Si preguntan por calorías o nutrición, mostrar links directamente
    elif re.search(r"(calorías|calorias|nutrición|nutricional)", user_input, re.IGNORECASE):
        st.chat_message("assistant").markdown("""
Lamentablemente, no tengo disponible el dato exacto de calorías en este momento.  
Sin embargo, te recomiendo consultar estos enlaces oficiales:

👉 [Menú y productos en la web de Bembos](https://www.bembos.com.pe/menu)  
📱 [App en Google Play](https://play.google.com/store/apps/details?id=pe.bembos.app&hl=es&gl=US)  
📱 [App en iOS (Apple)](https://apps.apple.com/pe/app/bembos/id6443560162)
        """)

    # --- Si pasa el filtro, enviar al modelo
    else:
        st.session_state.chat.send_message(user_input)
        response = st.session_state.chat.last.text
        st.chat_message("assistant").markdown(response)
