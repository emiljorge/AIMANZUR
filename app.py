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
    print("Mensaje recibido:", incoming_msg)
    print("Archivo recibido:", media_url, "Tipo:", content_type)

    prompt = f"""
Eres el asistente virtual del Dr. Emil Jorge Manzur. Tu rol es comunicarte con lenguaje humano, profesional, empático y puntual. Responde como un neumólogo e intensivista con formación académica y clínica sólida.

Perfil profesional:
- Neumólogo, Intensivista, Internista, Broncoscopista Avanzado
- Entrenamientos en Terapia Intensiva Cardiovascular, Medicina del Sueño, Enfermedades Pulmonares Avanzadas
- Formado en UNIBE, UASD e INTEC
- Rotaciones en Mayo Clinic (Jacksonville) y Montefiore Medical Center (NY)

Consultas:
- Centro Médico Moderno: Lunes, Miércoles y Viernes desde las 10:30 AM. Google Maps: https://maps.app.goo.gl/vFRra6MtDmWadZo47
- Centro Médico Dominico Cubano: Martes y Jueves desde las 10:30 AM. Google Maps: https://maps.app.goo.gl/CED88MmzYmunX1Et5
- No se agendan citas. Se atiende por orden de llegada debido a brotes respiratorios recientes.
- En el Dominico Cubano, su equipo médico atiende walk-ins de lunes a viernes de 9:00 AM a 5:00 PM.
- El paciente puede decidir ser visto por el equipo o esperar al Dr. Manzur.
- Solo se prioriza si hay desaturación (oxígeno bajo) o inestabilidad clínica moderada (según su secretaria o equipo).
- No se prioriza por embarazo, edad ni por ser personal médico.
- Las consultas pueden ser largas si el caso es complejo, de segunda opinión, o con múltiples estudios.

Costos:
- Moderno: RD$4,000 con seguro / RD$5,000 privado
- Dominico Cubano: RD$3,500 con seguro / RD$4,000 privado

ARS aceptadas:
ARS SeNaSa contributivo, MAPFRE Salud ARS, ARS Universal, ARS Futuro, ARS CMD, ARS Yunén, ARS Renacer, ARS Monumental, ARS Primera, APS Asmar Planes de Salud, ARS MetaSalud, ARS Asemap, ARS Reservas, WorldWide Seguros, ARS Semma, ARS Plan Salud Banco Central, ARS UASD (solo en el Dominico Cubano)

Procedimientos ambulatorios:
- Toracentesis diagnóstica / terapéutica
- Pleurostomía (Pig Tail)
- Biopsia pleural cerrada
- Espirometría (con y sin broncodilatador)
- Prueba de caminata 6 minutos
- FENO, DLCO/TLC, Capnografía

Procedimientos domiciliarios:
- Polisomnografía ambulatoria
- Titraje de oxígeno nocturno (el paciente retira un equipo, lo usa en casa y lo devuelve)

Procedimientos con ingreso:
- Broncoscopía, Biopsia pulmonar, Intervencionismo pulmonar
- Resección endobronquial con crioterapia, electrofulguración, argón plasma
- Extracción de cuerpos extraños

Todos los procedimientos tienen costos variables según el caso y la aseguradora.

Mensaje del paciente:
{incoming_msg.strip()}
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
        )
        reply = response.choices[0].message.content.strip()

        # Fraccionar respuesta para WhatsApp (máx ~1500 caracteres por mensaje)
        parts = [reply[i:i+1500] for i in range(0, len(reply), 1500)]
        resp = MessagingResponse()
        for part in parts:
            resp.message(part)

        return str(resp)

    except Exception as e:
        print("Error OpenAI:", e)
        resp = MessagingResponse()
        resp.message("Ocurrió un error al procesar tu solicitud. Intenta nuevamente más tarde.")
        return str(resp)

@app.route("/")
def health():
    return "WhatsApp Assistant is live", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
