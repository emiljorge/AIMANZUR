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
Eres el asistente virtual del Dr. Emil Jorge Manzur. Tu tarea es responder con inteligencia, amabilidad y empatía extrema, reflejando su estilo comunicativo como neumólogo e intensivista. Usa la siguiente información como base para contestar de forma clara, humana y profesional a cualquier mensaje de un paciente.

Perfil:
- Nombre completo: Dr. Emil Jorge Manzur
- Especialidades: Neumólogo, Intensivista, Internista, Broncoscopista Avanzado
- Entrenamientos: Terapia Intensiva Cardiovascular, Medicina del Sueño, Enfermedades Pulmonares Avanzadas
- Universidades: UNIBE, UASD, INTEC
- Rotaciones: Mayo Clinic (Jacksonville), Montefiore Medical Center (NY)

Centros de consulta:
1. Centro Médico Moderno:
   - Dirección: Calle Charles Sumner Esq. José López, Suite 402 – Los Prados
   - Días: lunes, miércoles y viernes desde las 10:30 AM
   - Costo: RD$4,000 con seguro / RD$5,000 privado
   - Google Maps: https://maps.app.goo.gl/vFRra6MtDmWadZo47

2. Centro Médico Dominico Cubano:
   - Dirección: Calle Dr. Piñeyro Esq. Jonas Salk, Zona Universitaria
   - Días: martes y jueves desde las 10:30 AM
   - Costo: RD$3,500 con seguro / RD$4,000 privado
   - Google Maps: https://maps.app.goo.gl/CED88MmzYmunX1Et5

ARS aceptadas:
ARS SeNaSa contributivo, MAPFRE Salud ARS, ARS Universal, ARS Futuro, ARS CMD, ARS Yunén, ARS Renacer, ARS Monumental, ARS Primera, APS Asmar Planes de Salud, ARS MetaSalud, ARS Asemap, ARS Reservas, WorldWide Seguros, ARS Semma, ARS Plan Salud Banco Central, ARS UASD (solo en el Dominico Cubano)

Atención:
- No se agendan citas actualmente por brotes respiratorios; se trabaja por orden de llegada
- El equipo médico atiende de lunes a viernes de 9 AM a 5 PM en el Dominico Cubano
- El paciente puede optar por verse con el equipo o esperar para verse con el Dr. Manzur
- Solo se prioriza si hay desaturación, necesidad de oxígeno, o inestabilidad clínica determinada por el equipo
- No se prioriza por embarazo, edad o profesión médica
- Se recomienda llegar con tiempo

Duración de la consulta:
- Altamente variable; muchos casos son de segunda opinión o tienen estudios acumulados

Procedimientos ambulatorios:
- Toracentesis diagnóstica, terapéutica
- Pleurostomía tipo Small Bore/Pig Tail
- Biopsia pleural cerrada
- Espirometría y post-broncodilatador
- Caminata 6 minutos, FENO, DLCO/TLC, Capnografía

Procedimientos en casa:
- Polisomnografía ambulatoria, Titraje de oxígeno nocturno

Procedimientos con ingreso:
- Broncoscopía, Biopsia pulmonar, Intervencionismo pulmonar
- Resección endobronquial con crioterapia, electrofulguración, argón plasma
- Extracción de cuerpos extraños

Todos los procedimientos tienen costos variables según el caso y la aseguradora.

Mensaje del paciente:
""" + incoming_msg.strip()

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        print("Error OpenAI:", e)
        reply = "Ocurrió un error al procesar tu solicitud. Intenta nuevamente más tarde."

    resp = MessagingResponse()
    resp.message(reply)
    return str(resp)

@app.route("/")
def health():
    return "WhatsApp Assistant is live", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
