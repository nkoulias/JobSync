import streamlit as st
import google.generativeai as genai
import os
import docx2txt
import PyPDF2 as pdf
from dotenv import load_dotenv
import streamlit.components.v1 as components


# Load environment variables from a .env file
load_dotenv()
# Set the favicon
st.set_page_config(page_title="ATS Resume Matching App", page_icon=":seedling:")

# Configure the generative AI model with the Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Set up the model configuration for text generation
generation_config = {
    "temperature": 0.6,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

# Define safety settings for content generation
safety_settings = [
    {"category": f"HARM_CATEGORY_{category}", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
    for category in ["HARASSMENT", "HATE_SPEECH", "SEXUALLY_EXPLICIT", "DANGEROUS_CONTENT"]
]


def generate_response_from_gemini(input_text):
     # Create a GenerativeModel instance with 'gemini-pro' as the model type
    llm = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings,
    )
    # Generate content based on the input text
    output = llm.generate_content(input_text)
    # Return the generated text
    return output.text

def extract_text_from_pdf_file(uploaded_file):
    # Use PdfReader to read the text content from a PDF file
    pdf_reader = pdf.PdfReader(uploaded_file)
    text_content = ""
    for page in pdf_reader.pages:
        text_content += str(page.extract_text())
    return text_content

def extract_text_from_docx_file(uploaded_file):
    # Use docx2txt to extract text from a DOCX file
    return docx2txt.process(uploaded_file)

# # Prompt Template
input_prompt_template = """
Using the resume, identify the top 5 skills mentioned that are most relevant to the requirements listed in the job description.
resume:{text}
description:{job_description}
I want the response in one single string having the structure
{{"Job Description Match":"%","Missing Keywords":"","Candidate Summary":"","Experience":""}}
"""

# # Streamlit app
# # Initialize Streamlit app
st.title("Resume Matching System")
job_description = st.text_area("Paste the Job Description",height=450)
uploaded_file = st.file_uploader("Upload Your Resume", type=["pdf", "docx"], help="Please upload a PDF or DOCX file")


# Handling the uploaded file
if uploaded_file is not None:
    file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type}
    # st.write(file_details)
    st.write("File uploaded successfully!")
    # You can add additional processing logic for the uploaded file here
else:
    st.write("Please upload a resume.")



submit_button = st.button("Submit")

if submit_button:
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            resume_text = extract_text_from_pdf_file(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            resume_text = extract_text_from_docx_file(uploaded_file)
        response_text = generate_response_from_gemini(input_prompt_template.format(text=resume_text, job_description=job_description))

        # Extract Missing Keywords from the response
        missing_keywords_start_key = '"Missing Keywords":"'
        start_mk_idx = response_text.find(missing_keywords_start_key) + len(missing_keywords_start_key)
        # Find the end position of the "Missing Keywords" value
        end_mk_idx = response_text.find('"', start_mk_idx)
        # Extract the keywords string
        keywords_str = response_text[start_mk_idx:end_mk_idx]
        # Split the extracted value into a list of keywords
        missing_keywords = keywords_str.split(', ')
        st.write(missing_keywords)
       
        # # Extract Match Percentage from the response
        # match_start_key = '"Job Description Match":"'
        # start_match_idx = response_text.find(match_start_key) + len(match_start_key)
        # # Find the end position of the "Missing Keywords" value
        # end_match_idx = response_text.find('"', start_match_idx)
        # # Extract the keywords string
        # match_str = response_text[start_match_idx:end_match_idx]
        # # Split the extracted value into a list of keywords
        # match_percentage = match_str.split(', ')
        # st.write(match_percentage)
        
        # Extract Candidate Summary from the response
        candidate_start_key = '"Candidate Summary":"'
        start_candidate_idx = response_text.find(candidate_start_key) + len(candidate_start_key)
        # Find the end position of the "Candidate Summary" value
        end_candidate_idx = response_text.find('"', start_candidate_idx)
        # Extract the keywords string
        candidate_str = response_text[start_candidate_idx:end_candidate_idx]
        st.write(candidate_str)
        
         # Extract Experience from the response
        exp_start_key = '"Experience":"'
        start_exp_idx = response_text.find(exp_start_key) + len(exp_start_key)
        # Find the end position of the "Candidate Summary" value
        end_exp_idx = response_text.find('"', start_exp_idx)
        # Extract the keywords string
        exp_str = response_text[start_exp_idx:end_exp_idx]
        st.write(exp_str)



        st.subheader("Resume Evaluation Result:")
        st.write(response_text)
        # st.write(f'{{\n"Job Description Match": "{match_percentage}%",\n"Missing Keywords": "{missing_keywords_str}",\n"Candidate Summary": "",\n"Experience": ""\n}}')
        # st.write(f'{{\n"Job Description Match": "{match_percentage}%"}}')

        # Display message based on Job Description Match percentage
        # if match_percentage >= 80:
        #     st.text("Move forward with hiring")
        # else:
        #     st.text("Your resume does not match the job description. Consider including more key words in your resume.")