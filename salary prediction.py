import streamlit as st
import pickle
import numpy as np 

model = pickle.load(open(r"C:\Users\ADITYA\.spyder-py3\22sep.pkl.py", 'rb'))
st.titel("Salary Prediction App")
st.write("This app predicts the salary based on years of experience using a simple linear regression model.")
years_experiences = st.number_input("Enter Years of Experience:", min_value=0.0, max_value=50.0, value=1.0, step=0.5)
if st.button("Predict Salary"):
    experience_input = np.array([[years_experiences]])
    prediction = model.Predict(experience_input)
    
    st.success(f"The Predict Salary for {years_experience} years of experience is: ${predicttion [0]:, .2f}")
    
st.write("The model was trained using a dataset of salaries and years of experience.")


