import streamlit as st
from streamlit_option_menu import option_menu
import pickle
import numpy as np
from fpdf import FPDF
import os

# Get working directory
working_dir = os.path.dirname(os.path.abspath(__file__))

# Load models
diabetes_model = pickle.load(open(f'{working_dir}/saved_models/diabetes_model.sav', 'rb'))
heart_disease_model = pickle.load(open(f'{working_dir}/saved_models/heart_disease_model.sav', 'rb'))
parkinsons_model = pickle.load(open(f'{working_dir}/saved_models/parkinsons_model.sav', 'rb'))

def generate_pdf(disease_name, inputs, prediction, advice, diet, exercise):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Medical Prediction Report", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"Disease: {disease_name}", ln=True)
    pdf.cell(200, 10, txt=f"Prediction Result: {'Positive' if prediction else 'Negative'}", ln=True)
    pdf.ln(10)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Input Details:", ln=True)
    pdf.set_font("Arial", size=12)
    for key, value in inputs.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Health Advice:", ln=True)
    pdf.set_font("Arial", size=12)
    for line in advice.split('\n'):
        pdf.cell(200, 10, txt=line, ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Recommended Diet:", ln=True)
    pdf.set_font("Arial", size=12)
    for line in diet.split('\n'):
        pdf.cell(200, 10, txt=line, ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Suggested Exercises:", ln=True)
    pdf.set_font("Arial", size=12)
    for line in exercise.split('\n'):
        pdf.cell(200, 10, txt=line, ln=True)

    output_path = os.path.join("Medical_Report.pdf")
    pdf.output(output_path)
    return output_path

# Sidebar
with st.sidebar:
    selected = option_menu(
        'Multiple Disease Prediction System',
        [
            'Diabetes Prediction',
            'Heart Disease Prediction',
            'Parkinsons Prediction'
        ],
        icons=['activity', 'heart', 'person'],
        default_index=0
    )

# Diabetes Prediction Page
if selected == 'Diabetes Prediction':
    st.title('Diabetes Prediction')

    col1, col2, col3 = st.columns(3)

    with col1:
        Pregnancies = st.text_input('Number of Pregnancies')

    with col2:
        Glucose = st.text_input('Glucose Level')

    with col3:
        BloodPressure = st.text_input('Blood Pressure value')

    with col1:
        SkinThickness = st.text_input('Skin Thickness value')

    with col2:
        Insulin = st.text_input('Insulin Level')

    with col3:
        BMI = st.text_input('BMI value')

    with col1:
        DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value')

    with col2:
        Age = st.text_input('Age of the Person')

    diagnosis = ''

    if st.button('Diabetes Test Result'):
        input_data = np.array([
            float(Pregnancies), float(Glucose), float(BloodPressure),
            float(SkinThickness), float(Insulin), float(BMI),
            float(DiabetesPedigreeFunction), float(Age)
        ]).reshape(1, -1)

        prediction = diabetes_model.predict(input_data)[0]
        diagnosis = 'The person is diabetic' if prediction else 'The person is not diabetic'

        st.success(diagnosis)

        report_path = generate_pdf("Diabetes", {
            "Pregnancies": Pregnancies,
            "Glucose": Glucose,
            "Blood Pressure": BloodPressure,
            "Skin Thickness": SkinThickness,
            "Insulin": Insulin,
            "BMI": BMI,
            "Diabetes Pedigree Function": DiabetesPedigreeFunction,
            "Age": Age
        }, prediction,
        "Maintain a healthy weight\nEat a balanced diet\nExercise regularly\nAvoid sugar-rich food",
        "Whole grains, leafy greens, lean protein\nLow sugar fruits like berries\nPlenty of water",
        "Brisk walking\nCycling\nYoga and stretching")

        st.download_button("Download Report", data=open(report_path, "rb"), file_name="Diabetes_Report.pdf")

# Heart Disease Prediction Page
if selected == 'Heart Disease Prediction':
    st.title('Heart Disease Prediction')

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.text_input('Age')

    with col2:
        sex = st.text_input('Sex (1 = male, 0 = female)')

    with col3:
        cp = st.text_input('Chest Pain types')

    with col1:
        trestbps = st.text_input('Resting Blood Pressure')

    with col2:
        chol = st.text_input('Serum Cholestoral in mg/dl')

    with col3:
        fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl (1 = true; 0 = false)')

    with col1:
        restecg = st.text_input('Resting Electrocardiographic results')

    with col2:
        thalach = st.text_input('Maximum Heart Rate achieved')

    with col3:
        exang = st.text_input('Exercise Induced Angina (1 = yes; 0 = no)')

    diagnosis = ''

    if st.button('Heart Disease Test Result'):
        input_data = np.array([
            float(age), float(sex), float(cp), float(trestbps), float(chol),
            float(fbs), float(restecg), float(thalach), float(exang)
        ]).reshape(1, -1)

        prediction = heart_disease_model.predict(input_data)[0]
        diagnosis = 'The person has heart disease' if prediction else 'The person does not have heart disease'

        st.success(diagnosis)

        report_path = generate_pdf("Heart Disease", {
            "Age": age,
            "Sex": sex,
            "Chest Pain": cp,
            "Resting BP": trestbps,
            "Cholestoral": chol,
            "Fasting BS": fbs,
            "ECG": restecg,
            "Max HR": thalach,
            "Exercise Angina": exang
        }, prediction,
        "Eat heart-healthy food\nAvoid smoking\nExercise regularly\nLimit alcohol and stress",
        "Low-sodium diet\nLean meats, nuts, fish\nFruits and vegetables",
        "Swimming\nCardio exercise\nLow-intensity aerobics")

        st.download_button("Download Report", data=open(report_path, "rb"), file_name="Heart_Report.pdf")

# Parkinsons Prediction Page
if selected == 'Parkinsons Prediction':
    st.title("Parkinson's Disease Prediction")

    col1, col2, col3 = st.columns(3)

    with col1:
        fo = st.text_input('MDVP:Fo(Hz)')

    with col2:
        fhi = st.text_input('MDVP:Fhi(Hz)')

    with col3:
        flo = st.text_input('MDVP:Flo(Hz)')

    with col1:
        jitter_percent = st.text_input('MDVP:Jitter(%)')

    with col2:
        shimmer = st.text_input('MDVP:Shimmer')

    with col3:
        apq3 = st.text_input('Shimmer:APQ3')

    with col1:
        apq5 = st.text_input('Shimmer:APQ5')

    with col2:
        apq = st.text_input('MDVP:APQ')

    with col3:
        dda = st.text_input('DDA')

    diagnosis = ''

    if st.button("Parkinson's Test Result"):
        input_data = np.array([
            float(fo), float(fhi), float(flo), float(jitter_percent),
            float(shimmer), float(apq3), float(apq5), float(apq), float(dda)
        ]).reshape(1, -1)

        prediction = parkinsons_model.predict(input_data)[0]
        diagnosis = "The person has Parkinson's disease" if prediction else "The person does not have Parkinson's disease"

        st.success(diagnosis)

        report_path = generate_pdf("Parkinson's", {
            "Fo": fo,
            "Fhi": fhi,
            "Flo": flo,
            "Jitter(%)": jitter_percent,
            "Shimmer": shimmer,
            "APQ3": apq3,
            "APQ5": apq5,
            "APQ": apq,
            "DDA": dda
        }, prediction,
        "See a neurologist regularly\nExercise often\nEat well and sleep enough\nStay mentally active",
        "High-fiber and antioxidant-rich foods\nAvoid processed food\nHydrate adequately",
        "Balance training\nStretching\nTai chi and yoga")

        st.download_button("Download Report", data=open(report_path, "rb"), file_name="Parkinson_Report.pdf")
