import streamlit as st
import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv('Heart_Disease_Dataset.csv')
    return df

# Preprocess the data
@st.cache_data
def preprocess_data(data):
    # Separate features and target
    X = data.drop('target', axis=1)
    y = data['target']
    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled, y, scaler

# Train the SVM model
@st.cache_data
def train_model(X, y):
    model = SVC(kernel='poly', degree=3)
    model.fit(X, y)
    return model

# Main function to run the Streamlit app
def main():
    st.title("Heart Disease Prediction")
    
    # Add a home page
    st.markdown(
        """
        Welcome to the Heart Disease Prediction Paradigm!
        
        This predicts the likelihood of heart disease based on various health parameters.
        
        Please enter your health information below and click the "Predict" button.
        """
    )

    # Load data
    data = load_data()
    X, y, scaler = preprocess_data(data)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)

    # Train the model
    model = train_model(X_train, y_train)

    # Collect user inputs
    st.header("Enter Your Information")
    age = st.slider("Age", min_value=20, max_value=100, value=50)
    sex = st.selectbox("Sex", ['Male', 'Female'])
    cp = st.selectbox("Chest Pain Type", ['Typical Angina', 'Atypical Angina', 'Non-anginal Pain', 'Asymptomatic'])
    trestbps = st.slider("Resting Blood Pressure (mmHg)", min_value=90, max_value=200, value=120)
    chol = st.slider("Cholesterol (mg/dl)", min_value=100, max_value=600, value=200)
    fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", ['True', 'False'])
    restecg = st.selectbox("Resting ECG", ['Normal', 'ST-T Wave Abnormality', 'Left Ventricular Hypertrophy'])
    thalach = st.slider("Maximum Heart Rate Achieved (bpm)", min_value=50, max_value=250, value=150)
    exang = st.selectbox("Exercise Induced Angina", ['Yes', 'No'])
    oldpeak = st.slider("ST Depression induced by exercise", min_value=0.0, max_value=6.2, value=0.0)
    slope = st.selectbox("Slope of the peak exercise ST segment", ['Upsloping', 'Flat', 'Downsloping'])

    # Convert categorical inputs to numerical
    sex = 1 if sex == 'Male' else 0
    cp_mapping = {'Typical Angina': 1, 'Atypical Angina': 2, 'Non-anginal Pain': 3, 'Asymptomatic': 4}
    cp = cp_mapping[cp]
    fbs = 1 if fbs == 'True' else 0
    restecg_mapping = {'Normal': 0, 'ST-T Wave Abnormality': 1, 'Left Ventricular Hypertrophy': 2}
    restecg = restecg_mapping[restecg]
    exang = 1 if exang == 'Yes' else 0
    slope_mapping = {'Upsloping': 1, 'Flat': 2, 'Downsloping': 3}
    slope = slope_mapping[slope]

    # Make prediction
    if st.button("Predict"):
        input_data = [[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope]]
        input_array = np.array(input_data)
        input_scaled = scaler.transform(input_array)
        prediction = model.predict(input_scaled)
        if prediction[0] == 0:
            st.write("Prediction: No Heart Disease")
        else:
            st.write("Prediction: Heart Disease Detected")

if __name__ == "__main__":
    main()
