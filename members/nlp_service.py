from collections import Counter
from django.db.models import Q
import spacy
import os
from members.models import Member, Patient, ChatResponse, Appointment, Encounter  # Import Django models

# Get the absolute path to the model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'members', 'spacy_model', 'clinic_nlp_model')

# Load the trained model
try:
    nlp = spacy.load(MODEL_PATH)
except Exception as e:
    nlp = None
    print(f"Error loading spaCy model: {e}")

# Function to query the database using Django ORM
# Get the absolute path to the model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'members', 'spacy_model', 'clinic_nlp_model')

# Load the trained model
try:
    nlp = spacy.load(MODEL_PATH)
except Exception as e:
    nlp = None
    print(f"Error loading spaCy model: {e}")

# Function to query the database using Django ORM
def query_database(entities):
    #https://chatgpt.com/c/67d66f73-9040-800a-92e4-e6fa7347a24b
    try:
        if not entities:
            return "Sorry, Unable to get information"

        # Count occurrences of each entity label
        entity_counts = Counter(label for _, label in entities)

        # Sort entity labels by frequency (most frequent first)
        sorted_labels = [label for label, _ in entity_counts.most_common()]
        print(f"sorted labels: {sorted_labels}")
        # Define model, search field, and response field based on entity labels
        entity_mapping = {
            "CLINIC": {"model": ChatResponse, "field": "question", "response_field": "answer"},
            "APPOINTMENT": {"model": Appointment, "field": "appointment_answer", "response_field": "appointment_answer"},
            "ENCOUNTER": {"model": Encounter, "field": "enc_answer", "response_field": "enc_answer"},
            "PHYSICIAN": {"model": Member, "field": "physician_answer", "response_field":"physician_answer"},
	    "INTEROGATIVE" :{"model": ChatResponse, "field": "question", "response_field": "answer"},	
	   ("PHYSICIAN", "PATIENT"): {"model": Encounter,"field": "enc_answer","response_field": "enc_answer" },
        }

        # Try each entity label in order of frequency
        for entity_label in sorted_labels:
            print(f"Entity :,{entity_label}")
            if entity_label not in entity_mapping:
                continue  # Skip unrecognized entities

            # Get relevant text for the current entity label
            relevant_texts = [text for text, label in entities if label == entity_label]
            print(f"Relevant Text : {relevant_texts}")
            model = entity_mapping[entity_label]["model"]
            search_field = entity_mapping[entity_label]["field"]
            response_field = entity_mapping[entity_label]["response_field"]

            # Construct an AND query using all relevant texts
            query = Q()
            for text in relevant_texts:
                query &= Q(**{f"{search_field}__icontains": text})
            print(f"query : {query}")
            # Perform the database search
            response = model.objects.filter(query).first()
            print(f"Response: {response}")
            if response:
                return getattr(response, response_field)  # Return first match and stop

        # If no relevant response is found in any entity table
        return "No relevant information found."

    except Exception as e:
        return f"Database error: {e}"
# Function to process text using the trained model
# Function to process text using the trained model
def process_text(text):
    if not nlp:
        return {"error": "Model not loaded"}
    
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    # Pass all extracted entities at once
    response = query_database(entities)  

    return {"entities": entities, "response": response if response else "No relevent data found"}  # Return first valid response