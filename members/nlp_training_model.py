# nlp_training_model.py
import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mchatbot.settings")
django.setup()

# Import required libraries
import spacy
from spacy.training.example import Example
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Training data
TRAIN_DATA = [
    ("Show me all appointments for Dr Sangita on 2nd March 2025", 
        {"entities": [(12,24,"APPOINTMENT"), (29, 39, "PHYSICIAN"), (43, 57, "DATE")]}),
    ("Tell me all appointments for Dr Manisha 6th March 2025", 
        {"entities": [(12,24,"APPOINTMENT"), (29, 39, "PHYSICIAN"), (40, 56, "DATE")]}),
    ("Provide appointment details for Dr Sanyal on 10th March 2025", 
        {"entities": [(8,19,"APPOINTMENT"), (32, 41, "PHYSICIAN"), (50, 66, "DATE")]}),
    ("What is the appointment details for Dr Kishor on 25th October 2025", 
        {"entities": [(0,4,"INTEROGATIVE"), (12,23,"APPOINTMENT"), (36, 45, "PHYSICIAN"), (50, 66, "DATE")]}),
]

# Load or create a blank NLP model
nlp = spacy.blank("en")  # Create a blank English NLP model

# Add Named Entity Recognizer (NER) if not already present
if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner", last=True)
else:
    ner = nlp.get_pipe("ner")

# Add entity labels to NER
ner.add_label("PHYSICIAN")
ner.add_label("APPOINTMENT")
ner.add_label("DATE")
ner.add_label("INTEROGATIVE")

# Convert training data into spaCy examples
examples = []
for text, annotations in TRAIN_DATA:
    doc = nlp.make_doc(text)
    example = Example.from_dict(doc, annotations)
    examples.append(example)

# Training loop
nlp.initialize()
for epoch in range(20):  # Train for 20 iterations
    losses = {}
    nlp.update(examples, losses=losses)
    print(f"Epoch {epoch + 1}, Loss: {losses}")

# Save trained model
model_path = os.path.join(os.getcwd(), "clinic_nlp_model")
nlp.to_disk(model_path)

# Send WebSocket message indicating training is complete
channel_layer = get_channel_layer()
async_to_sync(channel_layer.group_send)(
    "nlp_training", 
    {"type": "training.complete", "message": "NLP Training completed successfully!"}
)

print("Training completed and model saved!")