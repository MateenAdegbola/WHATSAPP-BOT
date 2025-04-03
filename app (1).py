from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace with your actual values
ACCESS_TOKEN = "EAAOfdqOajhcBOy1L9L9J5Q1RwCUwlr7wiaEVyHQks4q8zR2kK1JfZBlQwBeOvvvanrtus5DMPu9BZCYNzXg4217frdWFvFSRW5h4rD1ZBCctME2HacTqh7N3b5oGjCxkG56fPlFSzBK9M8ENYtQa1BbM3ZCZCifw8AcFyziD8noMs1GMOFr0VolU6tvACFzGLPqNOLykksxMoy3CNIP6kAobZCCP4ZD"
VERIFY_TOKEN = "VTU_TOKEN"
PHONE_NUMBER_ID = "473812242485192"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Verification process
        verify_token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if verify_token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Verification token mismatch", 403

    elif request.method == 'POST':
        # Handle incoming messages
        data = request.get_json()
        if data.get("object") == "whatsapp_business_account":
            for entry in data.get("entry", []):
                for change in entry.get("changes", []):
                    message_data = change.get("value").get("messages", [])
                    if message_data:
                        message = message_data[0]
                        phone_number = message["from"]
                        text = message.get("text", {}).get("body", "")
                        if text:
                            # Respond with a simple echo
                            send_message(phone_number, f"Echo: {text}")
        return "Message processed", 200

def send_message(phone_number, text):
    url = f"https://graph.facebook.com/v15.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {"body": text}
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print(f"Failed to send message: {response.status_code} - {response.text}")

if __name__ == '__main__':
    app.run(port=5000)
