import pickle
import numpy as np
from sklearn.tree import DecisionTreeClassifier

symptoms_list = [
    'fever', 'cough', 'headache', 'fatigue', 'body_pain',
    'sore_throat', 'runny_nose', 'chest_pain', 'shortness_of_breath',
    'nausea', 'vomiting', 'diarrhea', 'skin_rash', 'joint_pain', 'dizziness'
]

X = [
    # Flu — fever, cough, headache, fatigue, body_pain, sore_throat
    [1,1,1,1,1,1,0,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,0,0,0,0,0,0,0,0,0,0],
    [1,1,0,1,1,1,1,0,0,0,0,0,0,0,0],
    [1,0,1,1,1,1,0,0,0,0,0,0,0,0,0],

    # Common Cold — cough, sore_throat, runny_nose, fatigue
    [0,1,0,1,0,1,1,0,0,0,0,0,0,0,0],
    [0,1,0,0,0,1,1,0,0,0,0,0,0,0,0],
    [0,1,0,1,0,0,1,0,0,0,0,0,0,0,0],
    [0,0,0,1,0,1,1,0,0,0,0,0,0,0,0],

    # Pneumonia — fever, cough, chest_pain, shortness_of_breath, fatigue
    [1,1,0,1,1,0,0,1,1,0,0,0,0,0,0],
    [1,1,0,1,0,0,0,1,1,0,0,0,0,0,0],
    [1,1,0,0,1,0,0,0,1,0,0,0,0,0,0],
    [1,1,0,1,0,0,0,1,0,0,0,0,0,0,0],

    # Gastroenteritis — fever, nausea, vomiting, diarrhea, headache
    [1,0,1,1,0,0,0,0,0,1,1,1,0,0,0],
    [0,0,0,1,0,0,0,0,0,1,1,1,0,0,0],
    [1,0,0,0,0,0,0,0,0,1,1,1,0,0,0],
    [0,0,1,1,0,0,0,0,0,0,1,1,0,0,0],

    # Migraine — headache, nausea, dizziness, fatigue
    [0,0,1,1,0,0,0,0,0,1,0,0,0,0,1],
    [0,0,1,0,0,0,0,0,0,1,0,0,0,0,1],
    [0,0,1,1,0,0,0,0,0,0,0,0,0,0,1],
    [0,0,1,0,0,0,0,0,0,1,1,0,0,0,1],

    # Skin Allergy — skin_rash, fatigue
    [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
    [0,0,0,1,0,0,0,0,0,0,0,0,1,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0],
    [0,0,1,0,0,0,0,0,0,0,0,0,1,0,0],

    # Arthritis — joint_pain, fatigue, body_pain, dizziness
    [0,0,1,1,1,0,0,0,0,0,0,0,0,1,1],
    [0,0,0,1,1,0,0,0,0,0,0,0,0,1,0],
    [0,0,0,1,0,0,0,0,0,0,0,0,0,1,1],
    [0,0,1,0,1,0,0,0,0,0,0,0,0,1,0],

    # Heart Disease — chest_pain, shortness_of_breath, fatigue, dizziness
    [0,0,0,1,0,0,0,1,1,0,0,0,0,0,1],
    [0,0,0,1,0,0,0,1,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,1,0,0,0,0,0,1],
    [0,0,0,1,0,0,0,0,1,0,0,0,0,0,1],

    # Bronchitis — cough, chest_pain, fever, fatigue, sore_throat
    [1,1,0,1,1,1,0,1,1,0,0,0,0,0,0],
    [0,1,0,1,0,1,0,1,0,0,0,0,0,0,0],
    [1,1,0,1,0,0,0,1,1,0,0,0,0,0,0],
    [0,1,0,1,1,0,0,1,0,0,0,0,0,0,0],
]

y = [
    'Flu','Flu','Flu','Flu',
    'Common Cold','Common Cold','Common Cold','Common Cold',
    'Pneumonia','Pneumonia','Pneumonia','Pneumonia',
    'Gastroenteritis','Gastroenteritis','Gastroenteritis','Gastroenteritis',
    'Migraine','Migraine','Migraine','Migraine',
    'Skin Allergy','Skin Allergy','Skin Allergy','Skin Allergy',
    'Arthritis','Arthritis','Arthritis','Arthritis',
    'Heart Disease','Heart Disease','Heart Disease','Heart Disease',
    'Bronchitis','Bronchitis','Bronchitis','Bronchitis',
]

model = DecisionTreeClassifier(random_state=42)
model.fit(X, y)

with open('model/model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model trained successfully with", len(X), "samples!")
print("Diseases:", list(set(y)))