#14/10/2025 : START
import re
import pandas as pd
from fuzzywuzzy import fuzz

# Read Data from CSV
df = pd.read_csv('Data.csv')
# Keywords for each intent Convert CSV columns into Python dictionaries
intents = {row['intent']: row['keywords'].split('|') for _, row in df.iterrows()}

# Responses for each intent
responses = {row['intent']: row['response'] for _, row in df.iterrows()}

# --- Helper Functions ---
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text.split()

def find_intent(text):
    words = clean_text(text)
    best_intent, best_score = None, 0

    for intent, kw_list in intents.items():
        for kw in kw_list:
            for w in words:
                score = fuzz.ratio(w, kw)
                if score > best_score:
                    best_intent, best_score = intent, score

    return best_intent if best_score >= 70 else None

# --- Chat Loop ---
print("⚖️ Legal Chatbot — type 'exit' to quit\n")

while True:
    user = input("You: ")
    if user.lower() == "exit":
        print("Bot: Goodbye! Stay aware of your rights.")
        break

    intent = find_intent(user)
    if intent:
        print("Bot:", responses[intent])
    else:
        print("Bot: Sorry, I couldn’t understand. Could you rephrase?")
        
