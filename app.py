from dotenv import load_dotenv
import streamlit as st
import os
import io
import base64 
import fitz 
import google.generativeai as genai
import time

# load API
load_dotenv()

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

# Get AI respose 
def get_gemini_response(input,pdf_content, prompt) -> None:
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content["data"], prompt])
    return response.text

# Process the file and extract text 
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        pdf_document = fitz.open(stream = uploaded_file.read(), filetype = "pdf")

        pdf_text = ""
        for page in pdf_document:
            pdf_text += page.get_text("text") +"\n"
            
        pdf_parts = {"mime_type": "text/plain", "data":pdf_text}
        # first_page = pdf_document.load_page(0)

        # pix = first_page.get_pixmap()
        # img_bytes_arr = pix.tobytes()
        
        # pdf_parts = [
        #     {"mime_type":"image/jpeg",
        #      "data":base64.b64encode(img_bytes_arr).decode()}
        # ]
        
        return pdf_parts
    else:
        raise FileNotFoundError("No File Found")
    
st.set_page_config(page_title="Resume Fit", layout="centered")
# st.set_page_config(page_title="ATS Resume Expert")
# st.header("ATS RESUME EXPERT")
# input_text = st.text_area("Job Description", key = "input")
# uploaded_file = st.file_uploader("Upload Resume(PDF)",type=["pdf"])
st.markdown(
    """
    <style>
        .stTextArea textarea { font-size: 16px; }
        .stButton button { width: 100%; font-size: 18px; padding: 10px; }
        .stFileUploader label { font-size: 16px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📄 ResumeFit")
st.subheader("Optimize your resume for ATS systems!")

# Job description input
input_text = st.text_area("🔍 Paste the Job Description Below:", height=150, key="input")

# File uploader for resume
uploaded_file = st.file_uploader("📂 Upload Your Resume (PDF)", type=["pdf"])

# if uploaded_file is not None:
#     st.write("Uploading your PDF...")
#     progress_bar = st.progress(0)
    
#     for i in range(101):
#         time.sleep(0.01)  # Simulate upload time
#         progress_bar.progress(i)
    
#     st.success("PDF Uploaded Successfully!")
if uploaded_file:
    with st.spinner("Uploading your resume... Please wait!"):
        time.sleep(1)  # Simulating upload time
        st.success("✅ Resume uploaded successfully!")

col1, col2, col3 = st.columns(3)
submit1 = col1.button("Evaluate Resume")
submit2 = col2.button("Percentage Match")
submit3 = col3.button("Generate Questions")

input_prompt_1 = """You are an experienced HR with Tech Experience in the field of any job role from Data Science , Full stack Web Development, Big Data Engineering , DEVOPS, Data Analyst. Your task is to review the provided resume against the job description.
Please share your professional evaluation on whether the candidate's profile align with the provided job description and Highlight the strenghts and weakness of the applicant in relation to the specified job role. Keep the evaluation brief but still understandable
Split your feedback into 3 clearly seperated section
1. Strengths
2. Weakness
3. Recommendation
Also provide recommendation on resume structure, ATS-friendly formatting, and readability.
"""

input_prompt_2 = """You are an experienced HR with Tech Experience in the field of any job role from Data Science , Full stack Web Development, Big Data Engineering , DEVOPS, Data Analyst. Your task is to evaluate the resume against the provided job description.
Give me percentage match if the resume matches the job description.
First the output should come as percentage , then keywords missing and last final
Keep the evaluation brief
If job description is not added give percentage match for the one role you find the resume most suitable for"""

input_prompt_3 = """Based on the candidate's resume and the desired job role, please generate a set of 5 relevant interview questions to assess candidate's qualifications."""

def evaluation(input_prompt):
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)

        # Start Progress Bar (Fixing Delay Issue)
        progress_bar = st.progress(0)
        status_text = st.empty()
        status_text.write("⏳ Processing your resume...")

        # Simulate Real-time Progress
        for i in range(1, 101, 5):  # Increase progress in steps of 5
            time.sleep(0.05)  # Fast progress simulation
            progress_bar.progress(i)

        # Get AI response
        response = get_gemini_response(input_text, pdf_content, input_prompt)

        # End Progress Bar
        progress_bar.empty()
        status_text.success("✅ Analysis Complete!")

        # Display response
        st.subheader("📢 Your AI-Powered Resume Analysis:")
        st.write(response)
    else:
        st.warning("⚠️ Please upload your resume first!")

# Handle button clicks
if submit1:
    evaluation(input_prompt_1)
elif submit2:
    evaluation(input_prompt_2)
elif submit3:
    evaluation(input_prompt_3)