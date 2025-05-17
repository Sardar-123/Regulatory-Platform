#main2.py

import os
import streamlit as st
import pandas as pd
from ml.scoring import calculate_compliance_score
from ml.model_prediction import load_model_and_encoders, predict_compliance_score
from ml.query_retrieval import retrieve_context
from ml.generate_response import generate_response
from fpdf import FPDF
from data.weights.application_weights import application_weights, rating_scales

feedback_file_path = "data/feedback.csv"

# Ensure the directory exists
os.makedirs(os.path.dirname(feedback_file_path), exist_ok=True)

# Initialize session state for query and response
if "query" not in st.session_state:
    st.session_state.query = None
if "response" not in st.session_state:
    st.session_state.response = None

if "recommendations" not in st.session_state:
    st.session_state.recommendations = None

# Function to download files
def download_file(file_name, file_type):
    file_path = os.path.join("static", file_name)
    
    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            st.download_button(
                label=f"Download {file_name}",
                data=file,
                file_name=file_name,
                mime=file_type
            )
    else:
        st.error(f"File {file_name} not found.")

# Streamlit UI
st.title("Welcome to Regulatory Platform")

regulatory_option = st.selectbox(
    "Select Regulation",
    ["Select an Option", "SEPA", "DORA", "SWIFT"]
)

if regulatory_option == "SEPA":
    st.header("SEPA Compliance UI")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.image("static/bar.png", caption="SEPA Image 1")
    with col2:
        st.image("static/pie_chart.png", caption="SEPA Image 2")

    download_file("Detailed_Comparison_Report.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    download_file("IA_Report.pdf", "application/pdf")
    download_file("Test_Cases.pdf", "application/pdf")

elif regulatory_option == "DORA":
    st.title("DORA Compliance UI")

    rf_model, label_encoders, one_hot_columns = load_model_and_encoders()

    application_name = st.selectbox("Select Application Name", application_weights.keys())
    user_input = {feature: st.selectbox(feature, options) for feature, options in rating_scales.items()}

    if st.button("Generate Compliance Score and Recommendations"):
        input_data = pd.DataFrame([user_input])
        for column in input_data.columns:
            if column in label_encoders:
                input_data[column] = label_encoders[column].transform(input_data[column])
        for col in one_hot_columns:
            input_data[col] = 1 if f"App_{application_name}" == col else 0

        model_score = predict_compliance_score(rf_model, input_data, application_name, application_weights)
        rule_based_score = calculate_compliance_score(application_name, user_input, application_weights)

        st.markdown("<h3 style='color:black;'>Predicted DORA Compliance Score (Model):</h3>", unsafe_allow_html=True)
        st.markdown(
            f"<h3 style='color:{'green' if model_score > 70 else 'orange' if 50 <= model_score <= 70 else 'red'};'>{model_score:.2f}%</h3>",
            unsafe_allow_html=True
        )
        st.markdown("<h3 style='color:black;'>Predicted DORA Compliance Score (Rule-based):</h3>", unsafe_allow_html=True)
        st.markdown(
            f"<h3 style='color:{'green' if rule_based_score > 70 else 'orange' if 50 <= rule_based_score <= 70 else 'red'};'>{rule_based_score:.2f}%</h3>",
            unsafe_allow_html=True
        )

        query = f"Application: {application_name}\nInputs: {user_input}\nScores: Model={model_score:.2f}%, Rule-Based={rule_based_score:.2f}%"
        st.markdown("#### Query for Recommendations:")
        st.code(query)

        with st.spinner("Retrieving relevant documents using RAG..."):
            rag_context = retrieve_context(query, "C:/Users/mohds/Desktop/Project-2024/RP(12-05-2025)/embeddings/dora_index1", k=3)

        with st.spinner("Generating recommendations..."):
            recommendations = generate_response(query, "\n".join(rag_context), deployment_name="gpt-4")

        st.session_state.recommendations = recommendations
        st.write("### Generated Recommendations:")
        st.success(recommendations)

        from fpdf import FPDF

        def clean_text(text):
            replacements = {
                "‘": "'", "’": "'", "“": '"', "”": '"', "–": "-", "—": "-",
                "…" : "...", "•": "-", " ": " "
            }
            for old, new in replacements.items():
                text = text.replace(old, new)
            return text

        cleaned_recommendations = clean_text(recommendations)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_left_margin(10)
        pdf.set_right_margin(10)
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", "", 12)

        pdf.multi_cell(0, 10, txt=f"Application: {application_name}")
        pdf.multi_cell(0, 10, txt=f"Model Compliance Score: {model_score:.2f}%")
        pdf.multi_cell(0, 10, txt=f"Rule-Based Compliance Score: {rule_based_score:.2f}%")
        pdf.multi_cell(0, 10, txt="Recommendations:")
        pdf.multi_cell(0, 10, txt=cleaned_recommendations)

        pdf_file_path = "dora_compliance_recommendations.pdf"
        pdf.output(pdf_file_path)

        with open(pdf_file_path, "rb") as file:
            st.download_button(
                label="Download Recommendations",
                data=file,
                file_name="dora_compliance_recommendations.pdf",
                mime="application/pdf"
            )

    if st.session_state.recommendations:
        st.subheader("📝 Provide Feedback on the Response")
        feedback = st.radio("Was this response helpful?", ["Yes", "No"])
        comments = st.text_area("Additional Comments (Optional):")

        if st.button("Submit Feedback"):
            try:
                with open(feedback_file_path, "a") as f:
                    f.write(f"{st.session_state.query},{st.session_state.recommendations},{feedback},{comments}\n")
                st.success("Thank you for your feedback!")
            except Exception as e:
                st.error(f"Error saving feedback: {e}")

elif regulatory_option == "SWIFT":
    st.header("SWIFT Compliance")
    st.write("Work need to be done.")

st.markdown(
            """
            ---
            Powered by [Azure OpenAI](https://azure.microsoft.com/en-us/products/cognitive-services/openai-service/) and [LangChain](https://www.langchain.com/).
            """
        )
