import json
import random
from fastapi import APIRouter
from backend.schemas.chat_models import ChatResponse, ChatRequest
from backend.services.intent_processing import extract_entities, get_best_intent

router = APIRouter()

with open("backend/data/intents.json", "r") as file:
    intents_data = json.load(file)

all_intents = (
    intents_data.get("greetings", []) +
    intents_data.get("admin_intents", []) +
    intents_data.get("employee_intents", [])
)

@router.post("/process_chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    user_message = request.message.strip()
    intent, category, confidence = get_best_intent(user_message)
    entities = extract_entities(user_message)

    if intent == "unknown" or confidence < 0.3:
        return {
            "response": "Sorry, I didn’t understand that.",
            "intent": intent,
            "confidence": confidence,
            "entities": entities,
            "category": category,
        }

    intent_data = next((i for i in all_intents if i["tag"] == intent), None)
    
    if intent_data and "responses" in intent_data:
        response = random.choice(intent_data["responses"])
    else:
        response = "I'm sorry, I don't have a response for that."

    return {
        "response": response,
        "intent": intent,
        "confidence": confidence,
        "entities": entities,
        "category": category,
    }