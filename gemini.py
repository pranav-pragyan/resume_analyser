import streamlit as st
from secret import GOOGLE_API_KEY
import google.generativeai as genai
import pdfplumber
from prompt import match_percentage_prompt, conclusion_prompt
from PIL import Image

def extract_text_from_pdf(file):
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
    return text

class ResumeAnalyser:
    def __init__(self):
        # self.__prompt = prompt
        self.__gemini_api_key = GOOGLE_API_KEY
        genai.configure(api_key=self.__gemini_api_key)
        self.__model_name = "gemini-pro"
        self.__model = genai.GenerativeModel(self.__model_name)

    def get_response(self, prompt):
        response = self.__model.generate_content(prompt, generation_config=genai.types.GenerationConfig(temperature=1.0))
        return response.text

if __name__ == "__main__":
    resume_tracker = ResumeAnalyser() 

    st.header("Resume Analyser ")
    st.title("Get Insights of Resume According to Job Desription")

    job_desc = st.text_area("Enter Job Desription...", label_visibility="collapsed")
    uploaded_resume = st.file_uploader("select resume...", type=["pdf"])
    
    resume_content = ""
    if uploaded_resume:
        st.write("Resume Uploaded...")
        # st.write(str(uploaded_resume.read(), "utf-8"))
        resume_content = extract_text_from_pdf(uploaded_resume)
    
    col1, col2 = st.columns(2)
    with col1:
        match_percentage_button = st.button("Match Percentage...")
    
    with col2:
        conclusion_button = st.button("Get a conclusion...")
    
    if match_percentage_button:
        response = resume_tracker.get_response(match_percentage_prompt.format(job_desc = job_desc, resume = resume_content))
        st.subheader("The response is...")
        st.write(response)
        st.write("--"*20)
    
    if conclusion_button:
        response = resume_tracker.get_response(conclusion_prompt.format(job_desc = job_desc, resume = resume_content))
        st.subheader("Conclusion...")
        st.write(response)
        st.write("--"*20)

