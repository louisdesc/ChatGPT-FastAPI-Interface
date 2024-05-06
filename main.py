# main.py
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import uvicorn
from datetime import datetime
from openai import OpenAI
from chat_logic import import_txt_file, get_conversation_content, format_conversation, calculate_confidence, construct_prompt, verify_response

app = FastAPI()
templates = Jinja2Templates(directory="templates")
client = OpenAI()

# Define a global variable for the conversation number
CONVERSATION_NUMBER = 3

@app.get("/chat")
async def chat(request: Request):
    conversation = get_conversation_content(conversation_number=CONVERSATION_NUMBER)
    return templates.TemplateResponse("index.html", {"request": request, "conversation": conversation})

@app.post("/chat")
async def chat_with_assistant(request: Request, user_input: str = Form(...)):
    start_time = datetime.now()  # Start timing at the beginning of the function

    conversation = get_conversation_content(conversation_number=CONVERSATION_NUMBER)
    conversation.append({'role': 'user', 'content': user_input})
    formatted_conversation = format_conversation(conversation)
    predefined_responses = import_txt_file('data/reponses.txt')
    formatted_responses = "\n".join(predefined_responses)
    
    max_retries = 3  # Maximum number of retries
    is_valid_response = False
    ai_response = None
    confidence = 0
    for _ in range(max_retries):
        prompt = construct_prompt(formatted_conversation, formatted_responses)
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[{"role": "system", "content": prompt}],
            temperature=0,
            logprobs=True,
            top_logprobs=1,
            max_tokens=20
        )
        ai_response = completion.choices[0].message.content
        confidence = calculate_confidence(completion)
        
        is_valid_response = verify_response(ai_response, predefined_responses)
        if is_valid_response:
            break  # If the response is valid, exit the loop

    if not is_valid_response:
        print(ai_response)
        ai_response = "Je vais vous répondre." # Réponse par défaut

    end_time = datetime.now()  # End timing before forming the response
    total_response_time = (end_time - start_time).total_seconds()

    conversation.append({
        'role': 'assistant', 
        'content': ai_response, 
        'response_time': f"{total_response_time:.2f} seconds", 
        'confidence': f"{confidence:.2f}%"
    })

    return templates.TemplateResponse("index.html", {"request": request, "conversation": conversation})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
