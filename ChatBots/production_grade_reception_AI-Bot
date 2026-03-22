import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------------------
# TOOLS (FUNCTIONS)
# ---------------------------

def book_appointment(name, date, time):
    return {
        "status": "confirmed",
        "message": f"Appointment booked for {name} on {date} at {time}."
    }

def send_email(name, email, message):
    return {
        "status": "sent",
        "message": f"Email sent successfully to clinic from {name} ({email})."
    }

def contact_request(name, phone):
    return {
        "status": "received",
        "message": f"Our team will call {name} at {phone} shortly."
    }

# ---------------------------
# TOOL DEFINITIONS FOR GPT
# ---------------------------

tools = [
    {
        "type": "function",
        "function": {
            "name": "book_appointment",
            "description": "Book a dental appointment",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "date": {"type": "string"},
                    "time": {"type": "string"}
                },
                "required": ["name", "date", "time"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "Send an email to the clinic",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                    "message": {"type": "string"}
                },
                "required": ["name", "email", "message"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "contact_request",
            "description": "Request a callback from clinic",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "phone": {"type": "string"}
                },
                "required": ["name", "phone"]
            }
        }
    }
]

# ---------------------------
# SYSTEM PROMPT (IMPORTANT)
# ---------------------------

SYSTEM_PROMPT = """
You are a professional AI receptionist for a dental clinic.

Your goals:
- Help patients politely and professionally
- Understand flexible language
- Offer services like booking appointments, answering questions
- Use tools when needed

Rules:
- If user wants to book → call book_appointment
- If user wants contact → call contact_request
- If user wants to send message/email → call send_email
- Otherwise answer normally

Tone:
- Friendly, professional, concise
"""

# ---------------------------
# CHAT LOOP
# ---------------------------

def chat():
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    print("🦷 AI Dental Receptionist: Hello! How can I assist you today?")

    while True:
        user_input = input("You: ")

        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        msg = response.choices[0].message

        # ---------------------------
        # TOOL CALL HANDLING
        # ---------------------------
        if msg.tool_calls:
            for tool_call in msg.tool_calls:
                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                if function_name == "book_appointment":
                    result = book_appointment(**arguments)

                elif function_name == "send_email":
                    result = send_email(**arguments)

                elif function_name == "contact_request":
                    result = contact_request(**arguments)

                else:
                    result = {"error": "Unknown function"}

                messages.append(msg)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })

                # Second call after tool execution
                second_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages
                )

                final_msg = second_response.choices[0].message.content
                print("Bot:", final_msg)

                messages.append({"role": "assistant", "content": final_msg})

        else:
            print("Bot:", msg.content)
            messages.append({"role": "assistant", "content": msg.content})


if __name__ == "__main__":
    chat()
