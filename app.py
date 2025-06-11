import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

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


import re  # asegúrate de tener este import arriba

user_input = st.chat_input("¿Qué te apetece comer hoy?")

if user_input:
    st.chat_message("user").markdown(user_input)

    # --- Validación: solo responder si el mensaje está relacionado con Bembos ---
    temas_validos = [
        "bembos", "hamburguesa", "combo", "papas", "bebida", "postre",
        "menú", "ingredientes", "promoción", "calorías", "nutrición",
        "vegetariano", "sin gluten", "sin lactosa", "carne", "pollo"
    ]

    if not any(re.search(palabra, user_input, re.IGNORECASE) for palabra in temas_validos):
        respuesta = "Lo siento, no tengo información suficiente para ayudarte con esa solicitud. Solo puedo responder sobre productos y temas relacionados con **Bembos Perú**. 🍔"
        st.chat_message("assistant").markdown(respuesta)
    else:
        st.session_state.chat.send_message(user_input)
        response = st.session_state.chat.last.text
        st.chat_message("assistant").markdown(response)
