from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

VERIFY_TOKEN = "abba_verify_123"
PAGE_ACCESS_TOKEN = "IGAAUZBsqxiYWRBZAGJkdmtHVV9SX0kwb2dfMU1SUXFQMzhXWmVvODRuc3lBY1FxTE5kMlpHNHJ4b2ZAYaDZACbjVmamNOOTRjY1RCcVJQUy1VemxaakNhM0dHVVdCOGFtWVNkRmlsX09MdHhLMXFnYVFaVGpRcXdtR1ktLUZAiRTRpawZDZD"
# --- WEBHOOK VERIFY ---
@app.get("/webhook")
async def verify(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(challenge)

    return {"error": "Verification failed"}


# --- OPENAI ---
client = OpenAI()

SYSTEM_PROMPT = """
Sen Abba Web marketing agentligi uchun AI chatbot.

MAQSAD:
- klientni qiziqtirish
- xizmatlarni tushuntirish
- oxirida kontakt olish

TIL QOIDASI:
- User qaysi tilda yozsa, o‘sha tilda javob ber

QOIDALAR:
- 1-2 gapdan oshma
- oddiy va tushunarli yoz
- har doim oxirida savol ber

XIZMATLAR:
- Website (landing, korporativ, internet magazin)
- Branding
- SMM
- Marketing strategiya
- SEO va reklama

SOTUV:
- Qiziqsa → telefon so‘ra
- Tushunmasang → aniqlashtir

LEAD:
Qulay bo‘lsa, telefon raqamingizni qoldiring — siz bilan bog‘lanamiz.
"""

user_histories = {}

class Message(BaseModel):
    text: str
    user_id: str = "default_user"


def get_reply(user_id, user_message):
    if user_id not in user_histories:
        user_histories[user_id] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    user_histories[user_id].append({
        "role": "user",
        "content": user_message
    })

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=user_histories[user_id],
        temperature=0.5
    )

    reply = response.choices[0].message.content

    user_histories[user_id].append({
        "role": "assistant",
        "content": reply
    })

    return reply


# --- CHAT API ---
@app.post("/chat")
async def chat(msg: Message):
    try:
        if not msg.text:
            return {"reply": "Iltimos, savolingizni yozing."}

        reply = get_reply(msg.user_id, msg.text.strip())
        return {"reply": reply}

    except Exception as e:
        print("ERROR:", e)
        return {"reply": "Xatolik yuz berdi"}
        import requests

def send_message(user_id, text):
    url = f"https://graph.facebook.com/v19.0/me/messages?access_token={IGAAUZBsqxiYWRBZAGJkdmtHVV9SX0kwb2dfMU1SUXFQMzhXWmVvODRuc3lBY1FxTE5kMlpHNHJ4b2ZAYaDZACbjVmamNOOTRjY1RCcVJQUy1VemxaakNhM0dHVVdCOGFtWVNkRmlsX09MdHhLMXFnYVFaVGpRcXdtR1ktLUZAiRTRpawZDZD}"

    payload = {
        "recipient": {"id": user_id},
        "message": {"text": text}
    }

    requests.post(url, json=payload)
    import requests

@app.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    print("DATA:", data)

    if "entry" in data:
        for entry in data["entry"]:
            for change in entry.get("changes", []):
                value = change.get("value", {})
                messages = value.get("messages")

                if messages:
                    for msg in messages:
                        user_id = msg["from"]
                        text = msg["text"]["body"]

                        reply = get_reply(user_id, text)

                        send_message(user_id, reply)

    return {"status": "ok"}


def send_message(user_id, text):
    url = f"https://graph.facebook.com/v19.0/me/messages?access_token={IGAAUZBsqxiYWRBZAGJkdmtHVV9SX0kwb2dfMU1SUXFQMzhXWmVvODRuc3lBY1FxTE5kMlpHNHJ4b2ZAYaDZACbjVmamNOOTRjY1RCcVJQUy1VemxaakNhM0dHVVdCOGFtWVNkRmlsX09MdHhLMXFnYVFaVGpRcXdtR1ktLUZAiRTRpawZDZD}"

    payload = {
        "recipient": {"id": user_id},
        "message": {"text": text}
    }

    requests.post(url, json=payload)