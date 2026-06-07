from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import os

app = FastAPI()

# CORS - allows React to talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
class Message(BaseModel):
    text: str
    system: str = "You are a helpful assistant."

@app.post("/chat")
def chat(message: Message):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": message.system},
            {"role": "user", "content": message.text}
        ]
    )
    reply = response.choices[0].message.content
    return {"reply": reply}