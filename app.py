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
Eres el asistente virtual del Dr. Emil Jorge Manzur.

El Dr. Manzur es Neumólogo, Intensivista, Internista y Broncoscopista Avanzado. Tiene entrenamientos en Terapia Intensiva Cardiovascular, Medicina del Sueño y Enfermedades Pulmonares Avanzadas. Estudió en UNIBE, UASD e INTEC, y realizó rotaciones en Mayo Clinic (Jacksonville) y Montefiore Medical Center.

Consulta en:
- Centro Médico Moderno (lunes, miércoles y viernes desde 10:30 AM). Google Maps: https://maps.app.goo.gl/vFRra6MtDmWadZo47
- Centro Médico Dominico Cubano (martes y jueves desde 10:30 AM). Google Maps: https://maps.app.goo.gl/CED88MmzYmunX1Et5

Costos:
- Moderno: RD$4,000 con seguro / RD$5,000 privado
- Dominico Cubano: RD$3,500 con seguro / RD$4,000 privado

Aseguradoras aceptadas:
ARS SeNaSa contributivo, MAPFRE Salud ARS, ARS Universal, ARS Futuro, ARS CMD, ARS Yunén, ARS Renacer, ARS Monumental, ARS Primera, APS Asmar Planes de Salud, ARS MetaSalud, ARS Asemap, ARS Reservas, WorldWide Seguros, ARS Semma, ARS Plan Salud Banco Central y ARS UASD (solo en el Dominico Cubano).

Procedimientos ambulatorios:
- Toracentesis diagnóstica: Extracción de líquido del pulmón para análisis.
- Toracentesis terapéutica: Extracción de líquido para mejorar la respiración.
- Pleurostomía tipo Pig Tail: Drenaje del tórax.
- Biopsia pleural cerrada: Muestra del revestimiento del pulmón.
- Espirometría: Medición de la función pulmonar.
- Post-broncodilatador: Comparación antes y después del broncodilatador.
- Caminata 6 minutos: Evaluación de esfuerzo.
- FENO: Medición de inflamación en el asma.
- DLCO/TLC: Capacidad de difusión y volumen pulmonar.
- Capnografía: Evaluación del CO2 exhalado.

Procedimientos en casa:
- Polisomnografía ambulatoria: Estudio del sueño en el hogar.
- Titraje de oxígeno nocturno: Evaluación de oxigenación nocturna.

Procedimientos con ingreso:
- Broncoscopía: Evaluación directa de vías respiratorias.
- Biopsia de pulmón: Muestra de tejido pulmonar.
- Intervencionismo pulmonar: Procedimientos terapéuticos avanzados.
- Resección endobronquial con crioterapia, electrofulguración o argón plasma.
- Extracción de cuerpos extraños.

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
