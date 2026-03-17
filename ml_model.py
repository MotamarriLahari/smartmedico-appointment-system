import pickle
import os
from datetime import datetime

symptoms_list = [
    'fever', 'cough', 'headache', 'fatigue', 'body_pain',
    'sore_throat', 'runny_nose', 'chest_pain', 'shortness_of_breath',
    'nausea', 'vomiting', 'diarrhea', 'skin_rash', 'joint_pain', 'dizziness'
]

disease_to_specialty = {
    'Flu':              'General Physician',
    'Common Cold':      'General Physician',
    'Pneumonia':        'Pulmonologist',
    'Gastroenteritis':  'Gastroenterologist',
    'Migraine':         'Neurologist',
    'Skin Allergy':     'Dermatologist',
    'Arthritis':        'Orthopedic Surgeon',
    'Heart Disease':    'Cardiologist',
    'Bronchitis':       'Pulmonologist',
}

model_path = os.path.join(os.path.dirname(__file__), 'model', 'model.pkl')
with open(model_path, 'rb') as f:
    trained_model = pickle.load(f)

def predict_disease(selected_symptoms):
    input_vector = [1 if s in selected_symptoms else 0 for s in symptoms_list]
    prediction = trained_model.predict([input_vector])[0]
    specialty = disease_to_specialty.get(prediction, 'General Physician')
    return prediction, specialty

def predict_noshow(appointment_date, booking_date, appointment_time):
    try:
        appt        = datetime.strptime(str(appointment_date), '%Y-%m-%d')
        book        = datetime.strptime(str(booking_date), '%Y-%m-%d')
        lead_days   = (appt - book).days
        day_of_week = appt.weekday()
        hour        = int(str(appointment_time).split(':')[0])
        risk = 20
        if lead_days > 7:  risk += 30
        if lead_days > 14: risk += 20
        if day_of_week == 0: risk += 10
        if day_of_week == 4: risk += 10
        if hour < 9 or hour > 16: risk += 15
        return min(risk, 95)
    except:
        return 50