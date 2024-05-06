# chat_logic.py
import json
import math
from typing import List, Dict

# Import your predefined responses from a text file
def import_txt_file(file_path: str) -> List[str]:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().split('\n')

# Fetch the conversation content from a JSON file
def get_conversation_content(conversation_number: int, file_path: str = "data/conversations.json") -> List[Dict[str, str]]:
    with open(file_path, 'r') as f:
        conversations = json.load(f)
    if conversation_number < 1 or conversation_number > len(conversations):
        raise ValueError("Conversation number out of range")
    return [{"role": item["role"], "content": item["content"]} for item in conversations[conversation_number]]
 
# Format the conversation for display or processing
def format_conversation(conversation: List[Dict[str, str]]) -> str:
    return "\n".join([f"{conv['role']}: {conv['content']}" for conv in conversation])

# Calculate confidence from the completion response
def calculate_confidence(completion) -> float:
    total_logprob = 0
    count = 0
    for token_logprob in completion.choices[0].logprobs.content:
        total_logprob += token_logprob.top_logprobs[0].logprob
        count += 1
    average_logprob = total_logprob / count if count > 0 else 0
    overall_confidence = math.exp(average_logprob)
    return overall_confidence

# Check if the AI's response is in the predefined responses
def verify_response(ai_response: str, predefined_responses: List[str]) -> bool:
    return ai_response in predefined_responses

# Constructs the prompt
def construct_prompt(conversation: str, responses: str) -> str:
    PROMPT = """
    Historique de la conversation :
    {conversation}

    Ensemble de réponse prédéfinis :
    {reponses}

    Tâche :
    
    Sur la base de l'historique de la conversation, déterminer la réponse la plus appropriée à partir de l'ensemble des réponses prédéfinies.
    La réponse choisie doit être directement pertinente à la dernière entrée de l'utilisateur dans l'historique.
    Ne répétez pas les réponses qui ont déjà été données dans l'historique de conversation.
    Fournissez uniquement la réponse prédéfinie correspondante, sans ajout ou modification.
    """
    return PROMPT.format(conversation=conversation, reponses=responses)

