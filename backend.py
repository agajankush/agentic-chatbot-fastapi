# 1. Setup Pydantic Model 9Schema Validation)
from pydantic import BaseModel
from typing import List

class RequestState(BaseModel):
    # Setup Data Contract in Pytdantic format
    # This ensures that the data coming in from Front end is in same format
    # Increases code maintainability and readability
    # This is the only allowed data format
    model_name: str 
    model_provider: str
    system_prompt: str
    messages: List[str]
    allow_search: bool

# 2. Setup AI from FrontEnd Request
from fastapi import FastAPI
from ai_agent import get_response

ALLOWED_MODEL_NAMES=["llama3-70b-8192", "mixtral-8x7b-32768", "llama-3.3-70b-versatile", "gpt-4o-mini"]

app=FastAPI(title="LangGraph AI agent")

@app.post("/chat")
def chat_endpoint(request: RequestState):
    """
    API Endpoint for the Chatbot
    """
    if request.model_name not in ALLOWED_MODEL_NAMES:
        return {"error": "Invalid model name.Kindly select a valid model."}

    llm_id = request.model_name
    query = request.messages
    allow_search = request.allow_search
    system_prompt = request.system_prompt
    provider = request.model_provider

    # Create AI Agent and get response
    response=get_response(llm_id, query, allow_search, system_prompt, provider)

    return response
# 3. Run app and Explore Swagger UI docs
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9999)