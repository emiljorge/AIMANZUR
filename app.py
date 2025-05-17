from flask import Flask, request, Response
import openai
import os
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

def detectar_categoria(texto):
    texto = texto.lower()
    if "hora" in texto or "día" in texto or "consultas" in texto:
        return "horario"
    elif "dónde" in texto or "ubicación" in texto or "queda" in texto:
        return "ubicacion"
    elif "cuánto" in texto or "precio" in texto or "tarifa" in texto:
        return "costo"
    elif "ars" in texto or "seguro" in texto or "aseguradora" in texto:
        return "seguros"
    elif "rehabilitación" in texto or "terapia respiratoria" in texto:
        return "rehabilitacion"
    elif "broncoscopia" in texto or "procedimiento" in texto or "estudio" in texto:
        return "procedimientos"
    elif "envío" in texto or "resultado" in texto or "mando" in texto:
        return "envio_resultados"
    elif "analiza" in texto or "interpreta" in texto or "hemograma" in texto:
        return "analisis_ia"
    else:
        return "otro"

respuestas = {
    "horario": "📅 Consultas:
- Centro Médico Moderno: lunes, miércoles y viernes desde las 10:30 AM.
- Centro Médico Dominico Cubano: martes y jueves desde las 10:30 AM.",
    "ubicacion": "📍 Ubicaciones:
- Centro Médico Moderno: Calle Charles Sumner Esq. José López, Suite 402 – Los Prados.
- Centro Médico Dominico Cubano: ver Google Maps.",
    "costo": "💰 Tarifas:
- Moderno: 4,000 con seguro / 5,000 privado
- Dominico Cubano: 3,500 con seguro / 4,000 privado",
    "seguros": "✅ Aceptamos ARS Humano y otras aseguradoras principales. Verifica tu plan antes de asistir.",
    "rehabilitacion": "🧘‍♂️ Ofrecemos terapia respiratoria, ejercicios funcionales, educación y seguimiento clínico.",
    "procedimientos": "🔬 Procedimientos: broncoscopía, espirometría, toracocentesis, estudios de sueño y más.",
    "envio_resultados": "📤 Puedes enviar estudios por WhatsApp o al correo neumomanzur@gmail.com.",
}

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.form.get("Body", "")
    media_url = request.form.get("MediaUrl0", "")
    content_type = request.form.get("MediaContentType0", "")
    print("Mensaje recibido:", incoming_msg)
    print("Archivo recibido:", media_url, "Tipo:", content_type)

    resp = MessagingResponse()
    categoria = detectar_categoria(incoming_msg)

    if categoria in respuestas:
        reply = respuestas[categoria]
    elif categoria == "analisis_ia" or media_url:
        prompt = f"Eres un médico neumólogo. Resume y explica este resultado médico:

'{incoming_msg}'"
        try:
            response = openai.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6,
            )
            reply = response.choices[0].message.content.strip()
        except Exception as e:
            print("Error OpenAI:", e)
            reply = "Ocurrió un error al analizar tus resultados. Intenta más tarde."
    else:
        reply = "Hola 👋 soy el asistente del Dr. Emil Manzur. ¿Cómo puedo ayudarte?"

    msg = resp.message(reply)

    if categoria == "otro":
        msg.body("Selecciona una opción:")
        msg.add_body_button("Horarios", "INFO_HORARIOS")
        msg.add_body_button("Ubicación", "INFO_UBICACION")
        msg.add_body_button("Costos", "INFO_COSTOS")

    return str(resp)

@app.route("/")
def health():
    return "WhatsApp Assistant is live", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
