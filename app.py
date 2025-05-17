from flask import Flask, request, Response
import openai
import os

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    from twilio.twiml.messaging_response import MessagingResponse

    incoming_msg = request.form.get("Body", "")
    sender = request.form.get("From", "")

    print("Mensaje recibido:", incoming_msg)

    if not incoming_msg:
        return "No message received", 400

    prompt = f"Eres el asistente virtual del Dr. Emil Manzur. Responde con lenguaje humano, claro y profesional al siguiente mensaje:\n\n'{incoming_msg}'"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        print("Error OpenAI:", e)
        reply = "Ocurrió un error al procesar el mensaje. Intenta más tarde."

    twiml = MessagingResponse()
    twiml.message(reply)
    return str(twiml)

@app.route("/voice", methods=["POST"])
def voice():
    from twilio.twiml.voice_response import VoiceResponse

    speech = request.form.get("SpeechResult", "")
    print("Speech received:", speech)

    prompt = f"Eres el asistente virtual del Dr. Emil Manzur. El paciente dijo: '{speech}'. Responde en tono amable, profesional y directo."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        print("Error OpenAI:", e)
        reply = "Lo siento, hubo un error al procesar tu mensaje. Intenta más tarde."

    twiml = VoiceResponse()
    twiml.say(reply, voice="es-US-Neural2-C", language="es-US")
    return Response(str(twiml), mimetype="text/xml")

@app.route("/")
def health():
    return "Assistant is live", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
