from fastapi import FastAPI
from backend.api import chat

app = FastAPI()

# Include chatbot API
app.include_router(chat.router, prefix="/api")

@app.get("/")
def home():
    return {"message": "Chatbot API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)