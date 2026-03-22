
                                        ###Dentist clinic reception Bot###
import json
import random
from rapidfuzz import fuzz

# Load knowledge base
with open("dentist_kb.json", "r") as file:
    data = json.load(file)

# Function to find best intent match
def find_best_match(user_input):
    best_score = 0
    best_intent = None

    user_input = user_input.lower()

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            score = fuzz.partial_ratio(user_input, pattern.lower())

            if score > best_score:
                best_score = score
                best_intent = intent

    return best_intent, best_score


# Smart fallback (instead of "I don't understand")
def fallback_response(user_input):
    return f"I'm not fully sure, but I think you're asking about \"{user_input}\".\nCould you please give a bit more detail so I can help better?"


# Chat loop
def chatbot():
    print("🦷 Dentist Reception Bot: Hello! How can I help you today?")

    while True:
        user_input = input("You: ")

        if user_input.strip() == "":
            continue

        intent, score = find_best_match(user_input)

        # Flexible threshold
        if score > 60:
            response = random.choice(intent["responses"])
        else:
            response = fallback_response(user_input)

        print("Bot:", response)

        if intent and intent["tag"] == "closing":
            break


if __name__ == "__main__":
    chatbot()
