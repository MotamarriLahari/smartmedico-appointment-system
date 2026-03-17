import pickle
import numpy as np
from sklearn.tree import DecisionTreeClassifier

symptoms_list = [
    'fever', 'cough', 'headache', 'fatigue', 'body_pain',
    'sore_throat', 'runny_nose', 'chest_pain', 'shortness_of_breath',
    'nausea', 'vomiting', 'diarrhea', 'skin_rash', 'joint_pain', 'dizziness'
]

X = [
    [1,1,1,1,1,1,1,0,0,0,0,0,0,0,0],
    [0,1,0,1,0,1,1,0,0,0,0,0,0,0,0],
    [1,1,0,1,1,0,0,1,1,0,0,0,0,0,0],
    [1,0,1,1,0,0,0,0,0,1,1,1,0,0,0],
    [0,0,1,1,0,0,0,0,0,1,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
    [0,0,1,1,1,0,0,0,0,0,0,0,0,1,1],
    [0,0,0,1,0,0,0,1,1,0,0,0,0,0,1],
    [1,1,0,1,1,1,0,1,1,0,0,0,0,0,0],
]

y = [
    'Flu',
    'Common Cold',
    'Pneumonia',
    'Gastroenteritis',
    'Migraine',
    'Skin Allergy',
    'Arthritis',
    'Heart Disease',
    'Bronchitis',
]

model = DecisionTreeClassifier()
model.fit(X, y)

with open('model/model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model trained and saved to model/model.pkl successfully!")