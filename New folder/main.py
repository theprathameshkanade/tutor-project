import streamlit as st   # type: ignore
import google.generativeai as genai # type: ignore
from dotenv import load_dotenv # type: ignore
import os

# Streamlit Page Config
st.set_page_config(
    page_title="AI Learning Buddy", 
    page_icon="🤖", 
    layout="wide"
)

# Load API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# Initialize Gemini Model
model = genai.GenerativeModel('gemini-1.5-flash')

# Custom Styling
st.markdown("""
<style>
    .gradient-header {
        background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem 0.5rem 0 0;
    }
    .history-card {
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# Helper to generate responses
def get_response(prompt, difficulty="intermediate"):
    difficulty_prompts = {
        "beginner": "Explain this in simple terms for a beginner: ",
        "intermediate": "Provide a detailed explanation of: ",
        "advanced": "Give an in-depth technical analysis of: "
    }

    full_prompt = f"{difficulty_prompts[difficulty]}{prompt}"
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Save to session state history
def save_to_history(question, answer):
    if 'history' not in st.session_state:
        st.session_state.history = []
    st.session_state.history.append({
        "question": question,
        "answer": answer
    })


# ========== Streamlit UI Starts ==========

with st.container():
    st.markdown('<div class="gradient-header"><h1>AI Learning Buddy</h1></div>', unsafe_allow_html=True)

    with st.sidebar:
        st.header("Settings")
        difficulty = st.select_slider(
            "Select difficulty level",
            options=["beginner", "intermediate", "advanced"],
            value="intermediate",
            key="difficulty_slider"
        )

    tab1, tab2, tab3 = st.tabs(["📚 Learn", "🧩 Quiz", "📈 Review"])

    # Learn Tab
    with tab1:
        st.header("Learn Something New")
        user_prompt = st.text_area(
            "What would you like to learn about?",
            key="learn_prompt",
            height=100
        )
        
        if st.button("Get Answer", key="learn_button", use_container_width=True):
            if user_prompt:
                with st.spinner("Generating response..."):
                    response = get_response(user_prompt, difficulty)
                    if response:
                        st.success("Here's your explanation:")
                        st.write(response)
                        save_to_history(user_prompt, response)
            else:
                st.warning("Please enter a question")

    # Quiz Tab
    with tab2:
        st.header("Generate Quiz")
        quiz_topic = st.text_input(
            "Enter a topic for a quick quiz:",
            key="quiz_topic"
        )
        
        if st.button("Generate Quiz", key="quiz_button", use_container_width=True):
            if quiz_topic:
                with st.spinner("Creating your quiz..."):
                    quiz_prompt = f"Create a 3-question quiz about {quiz_topic} suitable for {difficulty} level"
                    quiz = get_response(quiz_prompt, difficulty)
                    if quiz:
                        st.success("Here's your quiz:")
                        st.write(quiz)
            else:
                st.warning("Please enter a topic for the quiz")

    # History Tab
    with tab3:
        st.header("Learning History")
        if 'history' not in st.session_state or len(st.session_state.history) == 0:
            st.info("No history available yet. Start learning to see your previous topics here!")
        else:
            for i, item in enumerate(st.session_state.history):
                with st.expander(f"Topic {i+1}", expanded=False):
                    st.markdown(f"""
                    <div class="history-card">
                        <h4>Question:</h4>
                        <p>{item['question']}</p>
                        <h4>Answer:</h4>
                        <p>{item['answer']}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        if st.button("Clear History", key="clear_history", use_container_width=True):
            st.session_state.history = []
            st.success("History cleared successfully!")
