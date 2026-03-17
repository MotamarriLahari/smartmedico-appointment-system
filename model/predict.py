import pickle
import os

symptoms_list = [
    'fever', 'cough', 'headache', 'fatigue', 'body_pain',
    'sore_throat', 'runny_nose', 'chest_pain', 'shortness_of_breath',
    'nausea', 'vomiting', 'diarrhea', 'skin_rash', 'joint_pain', 'dizziness'
]

disease_to_specialty = {
    'Flu':              'General Physician',
    'Common Cold':      'General Physician',
    'Pneumonia':        'General Physician',
    'Gastroenteritis':  'General Physician',
    'Migraine':         'General Physician',
    'Skin Allergy':     'Dermatologist',
    'Arthritis':        'General Physician',
    'Heart Disease':    'Cardiologist',
    'Bronchitis':       'General Physician',
}

model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
with open(model_path, 'rb') as f:
    model = pickle.load(f)

def predict_disease(selected_symptoms):
    input_vector = [1 if s in selected_symptoms else 0 for s in symptoms_list]
    prediction = model.predict([input_vector])[0]
    specialty = disease_to_specialty.get(prediction, 'General Physician')
    return prediction, specialty