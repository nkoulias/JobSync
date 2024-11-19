import streamlit as st
import openai

openai.api_key = 'sk-proj-qTkGi4FM6ox6nwFb92hvT3BlbkFJVJMPco3Cgfkvrkqbj3rg'
import PyPDF2 as pdf

# Set your OpenAI API key
st.set_page_config(page_title="ATS Resume Matching App", page_icon=":seedling:")

def extract_text_from_pdf_file(uploaded_file):
    # Use PdfReader to read the text content from a PDF file
    pdf_reader = pdf.PdfReader(uploaded_file)
    text_content = ""
    for page in pdf_reader.pages:
        text_content += str(page.extract_text())
    return text_content

def compare_resume_to_job_description(resume_text, job_description):
    prompt = f"""
    I have a resume and a job description. Please analyze how well the resume matches the job description. 
    Provide a match percentage and highlight the strengths and weaknesses of the resume in relation to the job description.

    Job Description:
    {job_description}

    Resume:
    {resume_text}
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant that helps match resumes to job descriptions."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )

    return response.choices[0].message['content'].strip()

# Streamlit UI
st.title('Resume to Job Description Matcher')

job_description = st.text_area("Enter Job Description", height=250)

uploaded_file = st.file_uploader("Upload Resume PDF", type="pdf")
submit_button = st.button("Compare Resume to Job Description")

if submit_button:
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            resume_text = extract_text_from_pdf_file(uploaded_file)
            # st.write(resume_text)
            match_result = compare_resume_to_job_description(resume_text, job_description)
            st.write("Match Analysis Result:")
            st.write(match_result)