from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()
client = OpenAI()

SYSTEM_PROMPT = """
Sen Abba Web marketing agentligi uchun AI chatbot.

MAQSAD:
- klientni qiziqtirish
- xizmatlarni tushuntirish
- oxirida kontakt olish

TIL QOIDASI:
- User qaysi tilda yozsa, o‘sha tilda javob ber
- Uzbek → Uzbek
- Russian → Russian
- English → English
- Hech qachon "men bu tilda gaplasha olmayman" deb yozma

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


@app.post("/chat")
async def chat(msg: Message):
    try:
        if not msg.text:
            return {"reply": "Iltimos, savolingizni yozing."}

        user_text = msg.text.strip()
        user_id = msg.user_id

        reply = get_reply(user_id, user_text)

        return {"reply": reply}

    except Exception as e:
        print("ERROR:", e)
        return {"reply": "Xatolik yuz berdi"}