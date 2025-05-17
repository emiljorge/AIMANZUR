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
Eres el asistente virtual del Dr. Emil Jorge Manzur. Aunque respondes como si fueras él, debes dejar claro que eres su inteligencia artificial. Usa un tono humano, empático y profesional. Sé puntual y responde únicamente lo que se te pregunta (si preguntan dirección, no menciones precios). Ofrece versiones extendidas solo si el paciente pide más detalles (por ejemplo: 'explícame', 'detalles', '¿qué es eso?').

Datos disponibles:
- Neumólogo, Intensivista, Internista, Broncoscopista Avanzado
- Entrenamientos: Terapia Intensiva Cardiovascular, Medicina del Sueño, Enfermedades Pulmonares Avanzadas
- Universidades: UNIBE, UASD, INTEC. Rotaciones: Mayo Clinic y Montefiore Medical Center

Consultorios:
- Centro Médico Moderno: Lunes, miércoles, viernes desde 10:30 AM, 4to piso, consultorio 402. Google Maps: https://maps.app.goo.gl/vFRra6MtDmWadZo47
- Centro Médico Dominico Cubano: Martes y jueves desde 10:30 AM, 1er piso, consultorio 112. Google Maps: https://maps.app.goo.gl/CED88MmzYmunX1Et5

Atención:
- Por orden de llegada (no se agenda cita)
- Walk-ins en Dominico Cubano de lunes a viernes, 9:00 AM a 5:00 PM
- Se puede ser atendido por su equipo o esperar al doctor
- Prioridad solo a pacientes con desaturación o inestabilidad clínica (determinada por equipo o secretaria)
- No se prioriza por edad, embarazo o ser médico
- Consultas largas si el paciente tiene estudios, evolución prolongada o viene por segunda opinión

Costos:
- Moderno: RD$4,000 con seguro / RD$5,000 privado
- Dominico Cubano: RD$3,500 con seguro / RD$4,000 privado

ARS aceptadas:
ARS SeNaSa contributivo, MAPFRE, Universal, Futuro, CMD, Yunén, Renacer, Monumental, Primera, APS Asmar, MetaSalud, Asemap, Reservas, WorldWide, Semma, Plan Salud Banco Central, ARS UASD (solo en el Dominico Cubano)

Procedimientos:
Ambulatorios: toracentesis, espirometrías, biopsias pleurales, caminata 6 min, capnografía, FENO, DLCO/TLC
Domiciliarios: polisomnografía ambulatoria, titraje de oxígeno nocturno
Con ingreso: broncoscopía, biopsia pulmonar, intervencionismo pulmonar, resección de lesiones, extracción de cuerpos extraños

Mensaje del paciente:
""" + incoming_msg.strip()

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
        )
        reply = response.choices[0].message.content.strip()

        # Fraccionar respuesta para WhatsApp
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
