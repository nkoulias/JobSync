import streamlit as st
import openai
import PyPDF2
import os


# Set your OpenAI API key
# openai.api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = 'sk-proj-qTkGi4FM6ox6nwFb92hvT3BlbkFJVJMPco3Cgfkvrkqbj3rg'

# Hide the settings and menu buttons using CSS
st.set_page_config(page_title="JobSync", page_icon=":seedling:", menu_items=None)
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .css-1q8dd3e {visibility: hidden;}
    .css-18ni7ap.e8zbici2 {display: none !important;}
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfFileReader(pdf_file)
    text = ""
    for page_num in range(reader.numPages):
        page = reader.getPage(page_num)
        text += page.extract_text()
    return text

def is_valid_job_description(job_description):
    # Minimum length check
    if len(job_description) < 50:
        return False, "Job description is too short to be valid."
    
    # Keyword check (you can customize this list based on your needs)
    professional_keywords = ["experience", "skills", "responsibilities", "requirements", "qualifications"]
    if not any(keyword in job_description.lower() for keyword in professional_keywords):
        return False, "Job description lacks professional keywords."
    
    return True, "Job description seems valid."

def compare_resume_to_job_description(resume_text, job_description):
    valid, message = is_valid_job_description(job_description)
    if not valid:
        return message, 0
    

def compare_resume_to_job_description(resume_text, job_description):
    prompt = f"""
    I have provided a job description and a resume. Please analyze how well the resume matches the job description. Firstly, please let me know if the job description doesn't make sense. 
    Secondly, provide a match percentage between the job description and resume. Finally, let me know what I can do to improve the resume to match the job description - only if the job description is of reasonable quality.

    Job Description:
    {job_description}

    Resume:
    {resume_text}
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are an assistant that helps match job descriptions to resumes."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )

    return response.choices[0].message['content'].strip()

# Streamlit UI
st.title('JobSync: Resume Compatibility Tool')

job_description = st.text_area("Enter Job Description", height=500)
# if job_description:
#     # Call the validation function and display the result
#     valid, validation_message = is_valid_job_description(job_description)
#     st.write(validation_message)

uploaded_file = st.file_uploader("Upload Resume PDF", type="pdf")

if uploaded_file is not None:
    resume_text = extract_text_from_pdf(uploaded_file)

    if st.button("Compare Resume to Job Description"):
        with st.spinner('Analyzing...'):
            match_result = compare_resume_to_job_description(resume_text, job_description)
            if job_description:
                valid, validation_message = is_valid_job_description(job_description)
                st.markdown(f"***{validation_message}***")
            st.subheader("Match Analysis Result:")
            st.write(match_result)