import streamlit as st
from groq import Groq
import os

# ==========================================
# Configuración de la Página
# ==========================================
st.set_page_config(
    page_title="Mi Chatbot IA",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Asistente Virtual (Powered by Groq)")
st.markdown("Este es un chatbot conversacional ultrarrápido usando el modelo **Llama 3**.")

# ==========================================
# Configuración de la API (Groq)
# ==========================================
# Intentamos leer la clave de los secretos de Streamlit
api_key = st.secrets.get("GROQ_API_KEY")

if not api_key:
    st.error("⚠️ Falta la API Key de Groq. Configúrala en los 'Secrets' de Streamlit.")
    st.stop()

client = Groq(api_key=api_key)

# ==========================================
# Gestión del Historial (Memoria)
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Eres un asistente útil, amable y profesional. Respondes siempre en español de manera concisa."}
    ]

# Mostrar historial en pantalla (saltando el mensaje del sistema)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# ==========================================
# Lógica del Chat
# ==========================================
if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    # 1. Mostrar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 2. Guardar en historial
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 3. Generar respuesta
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Llamada a Groq (Llama 3 8B es rapidísimo y gratis)
            chat_completion = client.chat.completions.create(
                messages=st.session_state.messages,
                model="llama3-8b-8192",
                temperature=0.5,
                max_tokens=1024,
                stream=True, # Efecto de escritura en tiempo real
            )

            for chunk in chat_completion:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
            # 4. Guardar respuesta del asistente
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"Ocurrió un error: {e}")