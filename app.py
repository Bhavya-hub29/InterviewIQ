import streamlit as st
from groq import Groq

# Configure Groq
client = Groq(api_key="PASTE_YOUR_KEY_HERE")

def ask_groq(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

st.set_page_config(page_title="Mock Interview Prep", page_icon="🎯")
st.title("🎯 Mock Interview Question Generator")
st.write("Paste a Job Description and practice your interview!")

jd = st.text_area("📋 Paste the Job Description here:", height=200)

if st.button("Generate Interview Questions"):
    if jd.strip() == "":
        st.warning("Please paste a Job Description first!")
    else:
        with st.spinner("Generating questions..."):
            prompt = f"""
You are an expert technical interviewer.
Based on the following Job Description, generate exactly 10 interview questions.
Mix technical and behavioral questions.
Number them 1 to 10.
Job Description:
{jd}
"""
            questions = ask_groq(prompt)
            st.session_state.questions = questions
            st.success("Questions generated!")

if "questions" in st.session_state:
    st.subheader("📝 Your Interview Questions:")
    st.write(st.session_state.questions)
    st.divider()
    st.subheader("✍️ Practice Your Answer:")
    question_input = st.text_input("Type the question you want to practice:")
    answer_input = st.text_area("Your Answer:", height=150)

    if st.button("Get Feedback on My Answer"):
        if answer_input.strip() == "":
            st.warning("Please type your answer first!")
        else:
            with st.spinner("Evaluating your answer..."):
                feedback_prompt = f"""
You are an expert interviewer. Evaluate this interview answer.
Question: {question_input}
Candidate's Answer: {answer_input}
Give:
1. Score out of 10
2. What was good
3. What to improve
4. A sample better answer
"""
                feedback = ask_groq(feedback_prompt)
                st.subheader("📊 Feedback:")
                st.write(feedback)