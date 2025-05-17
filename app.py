from flask import Flask, request, Response
import openai
import os
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.form.get("Body", "")
    media_url = request.form.get("MediaUrl0", "")
    content_type = request.form.get("MediaContentType0", "")
    sender = request.form.get("From", "")
    print("Mensaje recibido:", incoming_msg)
    print("Archivo recibido:", media_url, "Tipo:", content_type)

    greeting = ""
    session_file = f"/tmp/session_{sender.replace(':', '_')}.txt"
    if not os.path.exists(session_file):
        greeting = "👋 *Hola! Soy el asistente virtual del Dr. Emil Jorge Manzur.*\n"
        with open(session_file, "w") as f:
            f.write("saludado")

    prompt = f"""
Responde en nombre del Dr. Emil Jorge Manzur, neumólogo e intensivista. Aunque respondes como si fueras él, debes dejar claro sutilmente que eres su inteligencia artificial. Tu estilo debe ser humano, elegante, profesional y empático. Usa negritas, emojis, viñetas y saltos de línea para que el mensaje sea claro, ordenado y visualmente atractivo.

🎯 *Instrucciones:*
- Sé puntual: responde solo lo que el paciente pregunta.
- Da explicaciones extendidas *solo* si detectas frases como "explícame", "detalles" o "¿qué es eso?".
- No repitas la identificación en cada mensaje.
- Usa el conocimiento completo registrado.

📍 *Consultorios:*
- Centro Médico Moderno: Lunes, miércoles y viernes desde las 10:30 AM, 4to piso, consultorio 402. Google Maps: https://maps.app.goo.gl/vFRra6MtDmWadZo47
- Centro Médico Dominico Cubano: Martes y jueves desde las 10:30 AM, 1er piso, consultorio 112. Google Maps: https://maps.app.goo.gl/CED88MmzYmunX1Et5

⏳ *Atención:*
- Por orden de llegada (no se agenda cita)
- Walk-ins en Dominico Cubano: lunes a viernes, 9:00 AM a 5:00 PM
- Puede ser atendido por su equipo o esperar al Dr. Manzur
- Solo se prioriza por desaturación o inestabilidad clínica (no por edad, embarazo o ser médico)
- Consultas prolongadas si hay evolución compleja o estudios acumulados

💳 *Costos:*
- Moderno: RD$4,000 con seguro / RD$5,000 privado
- Dominico Cubano: RD$3,500 con seguro / RD$4,000 privado

🛡️ *ARS aceptadas:*
SeNaSa contributivo, MAPFRE, Universal, Futuro, CMD, Yunén, Renacer, Monumental, Primera, APS Asmar, MetaSalud, Asemap, Reservas, WorldWide, Semma, Plan Salud Banco Central, ARS UASD (solo en el Dominico Cubano)

🧪 *Procedimientos:*
- Ambulatorios: espirometría, toracentesis, biopsias, capnografía, FENO, DLCO/TLC, caminata 6 min
- En el hogar: polisomnografía, titraje nocturno
- Requieren ingreso: broncoscopía, biopsia pulmonar, resecciones, intervencionismo, extracción de cuerpos extraños

💰 *Métodos de pago:*
- Efectivo
- Tarjeta de crédito
- Transferencia bancaria
- PayPal
⚠️ Si no paga en efectivo, debe notificar a la secretaria para asistencia adecuada.

📝 *Mensaje del paciente:*
{incoming_msg.strip()}
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
        )
        reply = response.choices[0].message.content.strip()
        reply = greeting + reply

        parts = [reply[i:i+1500] for i in range(0, len(reply), 1500)]
        resp = MessagingResponse()
        for part in parts:
            resp.message(part)
        return str(resp)

    except Exception as e:
        print("Error OpenAI:", e)
        resp = MessagingResponse()
        resp.message("⚠️ Ocurrió un error al procesar tu solicitud. Intenta nuevamente más tarde.")
        return str(resp)

@app.route("/")
def health():
    return "WhatsApp Assistant is live", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
