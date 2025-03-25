import json
import os
import spacy
import nltk
from typing import Tuple, List
from rapidfuzz import fuzz  # Import fuzzy matching
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from backend.services.names_processing import get_names


# Load spaCy model
nlp = spacy.load("en_core_web_lg")

# Add Indian name entity recognition
ruler = nlp.add_pipe("entity_ruler", before="ner")
indian_names = get_names()
patterns = [{"label": "PERSON", "pattern": name} for name in indian_names]
ruler.add_patterns(patterns)

# Load intents JSON file
with open("backend/data/intents.json", "r") as file:
    intents_data = json.load(file)

vectorizer = TfidfVectorizer()


def preprocess_text(text: str) -> str:
    """Tokenize and preprocess user input."""
    return text.lower().strip()


def extract_entities(text: str) -> List[str]:
    """Extract named entities using spaCy."""
    doc = nlp(text.lower())
    return [{"name": ent.text, "label": ent.label_} for ent in doc.ents]


def get_best_intent(user_message: str) -> Tuple[str, str, float]:
    """Find the best intent along with its category using Fuzzy Matching + TF-IDF"""
    processed_message = preprocess_text(user_message)

    best_intent = None
    best_category = None
    highest_confidence = 0.0

    # Mapping categories to their intents
    intent_categories = {
        "greetings": intents_data.get("greetings", []),
        "admin_intents": intents_data.get("admin_intents", []),
        "employee_intents": intents_data.get("employee_intents", [])
    }

    for category, intents in intent_categories.items():
        for intent in intents:
            patterns = [preprocess_text(p) for p in intent["patterns"]]

            # **1️⃣ TF-IDF Similarity**
            all_texts = patterns + [processed_message]
            vectors = vectorizer.fit_transform(all_texts)

            similarities = cosine_similarity(
                vectors[-1], vectors[:-1]).flatten()
            max_similarity = max(similarities) if similarities.size > 0 else 0

            # **2️⃣ Fuzzy Matching (Levenshtein Distance)**
            fuzzy_scores = [fuzz.ratio(
                processed_message, pattern) / 100 for pattern in patterns]
            max_fuzzy = max(fuzzy_scores) if fuzzy_scores else 0

            # **Combine TF-IDF & Fuzzy Scores**
            final_confidence = max(max_similarity, max_fuzzy)

            if final_confidence > highest_confidence:
                highest_confidence = final_confidence
                best_intent = intent["tag"]
                best_category = category

    # If confidence is too low, return "unknown"
    if highest_confidence < 0.63:
        return "unknown", "unknown", 0.0

    return best_intent, best_category, highest_confidence
