import streamlit as st
import openai
import os
import time

# ✅ Set OpenAI API key
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]


# ✅ Fine-Tuned Model IDs
resume_model_id = "ft:gpt-3.5-turbo-0125:personal::BCuNaUa6"
cover_letter_model_id = "ft:gpt-3.5-turbo-0125:personal::BCuEOrPk"

# ✅ Function to Generate Text using Fine-Tuned Models
def generate_text(fine_tuned_model_id, prompt):
    """Generates text using the fine-tuned model."""
    response = openai.chat.completions.create(
        model=fine_tuned_model_id,
        messages=[{"role": "user", "content": prompt}],  # Provide prompt as a message
        max_tokens=500
    )
    return response.choices[0].message.content.strip()  # Access message content

# ✅ Streamlit UI
st.title("AI Resume & Cover Letter Generator")
st.markdown("🚀 **Generate professional resumes & cover letters with AI!**")

# ✅ User selects document type
option = st.radio("Select the type of document:", ["Resume", "Cover Letter"])

# ✅ User Inputs
job_title = st.text_input("Enter the job title you are applying for:", "")
company_name = st.text_input("Enter the company name:", "")
years_of_experience = st.number_input("Enter your total years of experience:", min_value=0, max_value=50, step=1)
past_roles = st.text_area("Enter your past titles and companies (comma-separated):", "")
job_description = st.text_area("Paste the job description:", "")

# ✅ Generate Button
if st.button("Generate"):
    if job_title and company_name and years_of_experience and past_roles and job_description:
        # Constructing the prompt dynamically
        user_prompt = f"""
        Based on this job description for a {job_title} role at {company_name}, write a {"resume" if option == "Resume" else "cover letter"} for my past {years_of_experience} years of work experience 
        with 3-5 bullet points per role that include metrics and the most important 10 keywords from the job description.
        My past titles and companies were {past_roles}. No need to include an objective statement.
        
        Job Description:
        {job_description}
        """

        model_id = resume_model_id if option == "Resume" else cover_letter_model_id
        with st.spinner("Generating... ⏳"):
            output = generate_text(model_id, user_prompt)
        
        st.subheader("Generated Output:")
        st.write(output)
    else:
        st.warning("⚠️ Please fill in all fields before generating.")

# ✅ Footer
st.markdown("---")
st.markdown("💡 **Powered by OpenAI Fine-Tuned Models** | Created with ❤️ using Streamlit")
