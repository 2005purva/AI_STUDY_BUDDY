import streamlit as st
import pandas as pd
from study_buddy import DocumentProcessor, RAGEngine, QuizGenerator

# Page Configuration
st.set_page_config(
    page_title="Smart AI Study Buddy & Quiz Generator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.3rem;
        font-weight: 700;
        color: #4A90E2;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        color: #6C757D;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
    }
    .card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.2rem;
        border-left: 5px solid #4A90E2;
        margin-bottom: 1rem;
    }
    .stButton>button {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "rag_engine" not in st.session_state:
    st.session_state.rag_engine = RAGEngine()
if "chunks" not in st.session_state:
    st.session_state.chunks = []
if "raw_text" not in st.session_state:
    st.session_state.raw_text = ""
if "quiz" not in st.session_state:
    st.session_state.quiz = []
if "flashcards" not in st.session_state:
    st.session_state.flashcards = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "quiz_scores" not in st.session_state:
    st.session_state.quiz_scores = {}

# Sidebar Navigation & Uploads
with st.sidebar:
    st.image("https://img.icons8.com/isometric/96/graduation-cap.png", width=70)
    st.title("📚 Study Material Hub")
    
    upload_type = st.radio("Choose Source Input:", ["📄 PDF Document", "📝 Plain Text / Lecture Notes"])
    
    document_text = ""
    
    if upload_type == "📄 PDF Document":
        uploaded_file = st.file_uploader("Upload textbook PDF or lecture slides", type=["pdf"])
        if uploaded_file is not None:
            with st.spinner("Extracting text from PDF..."):
                document_text = DocumentProcessor.extract_text_from_pdf(uploaded_file)
    else:
        document_text = st.text_area("Paste lecture notes or audio transcript below:", height=200, 
                                     placeholder="Paste your lecture notes, transcript, or study material here...")

    if st.button("🚀 Process Study Material", type="primary", use_container_width=True):
        if document_text.strip():
            with st.spinner("Chunking text & building RAG Knowledge Index..."):
                st.session_state.raw_text = document_text
                st.session_state.chunks = DocumentProcessor.chunk_text(document_text)
                st.session_state.rag_engine.index_chunks(st.session_state.chunks)
                
                # Generate Quiz & Flashcards
                st.session_state.quiz = QuizGenerator.generate_mcqs(st.session_state.chunks, num_questions=5)
                st.session_state.flashcards = QuizGenerator.generate_flashcards(st.session_state.chunks, max_cards=8)
                st.session_state.chat_history = []
                st.session_state.quiz_scores = {}
                
            st.success(f"Successfully processed {len(st.session_state.chunks)} study chunks!")
        else:
            st.warning("Please upload a PDF or paste text notes first.")

    st.markdown("---")
    st.markdown("### 📊 Material Stats")
    if st.session_state.chunks:
        st.metric("Total Chunks", len(st.session_state.chunks))
        st.metric("Generated Quiz Questions", len(st.session_state.quiz))
        st.metric("Flashcards Deck", len(st.session_state.flashcards))
    else:
        st.info("No study material loaded yet.")

# Main Dashboard Header
st.markdown('<div class="main-header">🎓 Smart AI Study Buddy & Quiz Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Transform your lecture notes, PDFs, and transcripts into instant quizzes, flashcards, and RAG tutor support.</div>', unsafe_allow_html=True)

if not st.session_state.chunks:
    st.info("👈 **Get Started:** Upload a study PDF or paste lecture notes in the sidebar on the left, then click **Process Study Material**.")
    
    # Sample Demo Content Option
    st.markdown("---")
    st.subheader("💡 Or Try With Demo Computer Science Notes:")
    if st.button("Load Sample Demo Material"):
        sample_notes = """
Artificial Intelligence (AI) is the simulation of human intelligence processes by machines, especially computer systems. 
Machine Learning (ML) is a subset of AI that provides systems the ability to automatically learn and improve from experience without being explicitly programmed.
Supervised Learning algorithms build a mathematical model of a set of data that contains both the inputs and the desired outputs. The data is known as training data, and consists of a set of training examples.
Unsupervised Learning algorithms take a set of data that contains only inputs, and find structure in the data, like grouping or clustering of data points.
Neural Networks are a set of algorithms, modeled loosely after the human brain, that are designed to recognize patterns. They interpret sensory data through a kind of machine perception, labeling or clustering raw input.
Deep Learning is part of a broader family of machine learning methods based on artificial neural networks with representation learning. Learning can be supervised, semi-supervised or unsupervised.
Overfitting is a concept in framework modeling where a statistical model begins to memorize noise and details in the training data rather than learning the generalized baseline.
Cross-validation is a resampling procedure used to evaluate machine learning models on a limited data sample.
"""
        st.session_state.raw_text = sample_notes
        st.session_state.chunks = DocumentProcessor.chunk_text(sample_notes)
        st.session_state.rag_engine.index_chunks(st.session_state.chunks)
        st.session_state.quiz = QuizGenerator.generate_mcqs(st.session_state.chunks, num_questions=5)
        st.session_state.flashcards = QuizGenerator.generate_flashcards(st.session_state.chunks, max_cards=8)
        st.rerun()

else:
    # Main Tabs Layout
    tab1, tab2, tab3, tab4 = st.tabs([
        "📚 Overview & Concepts", 
        "❓ Interactive Quiz", 
        "🃏 Flashcards Deck", 
        "🤖 24/7 RAG AI Tutor"
    ])

    # TAB 1: OVERVIEW & CONCEPTS
    with tab1:
        st.subheader("📌 Key Concepts Identified")
        concepts = DocumentProcessor.extract_key_concepts(st.session_state.raw_text, top_n=12)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("**Top Technical Terms:**")
            st.write(", ".join([f"`{c}`" for c in concepts]))
            
            st.markdown("**Raw Material Preview:**")
            st.text_area("Full Text Preview", st.session_state.raw_text[:1500] + "...", height=300, disabled=True)

        with col2:
            st.markdown("**Chunked Knowledge Base:**")
            for chunk in st.session_state.chunks[:4]:
                st.markdown(f"""
                <div class="card">
                    <b>Chunk #{chunk['id'] + 1}</b> ({chunk['length']} chars)<br>
                    <i>"{chunk['text']}"</i>
                </div>
                """, unsafe_allow_html=True)

    # TAB 2: INTERACTIVE QUIZ
    with tab2:
        st.subheader("❓ Practice Quiz (Multiple Choice)")
        if not st.session_state.quiz:
            st.warning("No quiz questions could be generated from this text. Try adding more detailed text.")
        else:
            score = 0
            total_questions = len(st.session_state.quiz)
            
            for q in st.session_state.quiz:
                st.markdown(f"#### {q['question']}")
                user_choice = st.radio(f"Select option for Question {q['id']}:", q['options'], key=f"q_{q['id']}")
                
                if st.button(f"Submit Answer for Q{q['id']}", key=f"btn_{q['id']}"):
                    if user_choice == q['answer']:
                        st.success(f"🎉 Correct! Answer: **{q['answer']}**")
                        st.session_state.quiz_scores[q['id']] = 1
                    else:
                        st.error(f"❌ Incorrect. Your answer: {user_choice}. Correct answer: **{q['answer']}**")
                        st.session_state.quiz_scores[q['id']] = 0
                    
                    with st.expander("💡 View Explanation"):
                        st.write(q['explanation'])
                
                st.markdown("---")

            # Final Score
            current_score = sum(st.session_state.quiz_scores.values())
            st.info(f"🏆 Current Quiz Score: **{current_score} / {total_questions}**")

    # TAB 3: FLASHCARDS DECK
    with tab3:
        st.subheader("🃏 Spaced Repetition Flashcards")
        if not st.session_state.flashcards:
            st.warning("No flashcards available.")
        else:
            card_idx = st.slider("Select Flashcard:", 1, len(st.session_state.flashcards), 1) - 1
            card = st.session_state.flashcards[card_idx]
            
            col_fc1, col_fc2 = st.columns([1, 1])
            with col_fc1:
                st.markdown("### ❓ FRONT (Question/Concept)")
                st.info(f"**{card['front']}**")
            
            with col_fc2:
                st.markdown("### 💡 BACK (Explanation)")
                if st.checkbox(f"Reveal Answer for Card #{card['id']}", key=f"fc_cb_{card['id']}"):
                    st.success(card['back'])
                else:
                    st.caption("Check the box above to flip the card.")

            # Spaced repetition status update
            st.markdown("#### Evaluate Your Recall:")
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            if col_btn1.button("🔴 Needs Review"):
                card['status'] = "Learning"
                st.toast(f"Card #{card['id']} marked for review.")
            if col_btn2.button("🟡 Good"):
                card['status'] = "Reviewing"
                st.toast(f"Card #{card['id']} updated.")
            if col_btn3.button("🟢 Mastered"):
                card['status'] = "Mastered"
                st.toast(f"Card #{card['id']} marked as Mastered!")

    # TAB 4: 24/7 RAG AI TUTOR
    with tab4:
        st.subheader("🤖 Grounded AI Study Tutor")
        st.caption("Ask questions strictly answered by your uploaded study notes.")
        
        user_query = st.text_input("Ask a question about your study material:", placeholder="e.g. What is supervised learning?")
        
        if st.button("Ask Tutor") and user_query:
            with st.spinner("Searching study material & generating answer..."):
                response_data = st.session_state.rag_engine.answer_question(user_query)
                
                st.session_state.chat_history.append({
                    "user": user_query,
                    "answer": response_data["answer"],
                    "sources": response_data["sources"]
                })
        
        # Render Chat History
        for chat in reversed(st.session_state.chat_history):
            st.markdown(f"**🙋 User:** {chat['user']}")
            st.markdown(f"**🤖 AI Tutor:**\n{chat['answer']}")
            
            if chat['sources']:
                with st.expander("🔍 View Context Sources & Citations"):
                    for src in chat['sources']:
                        st.caption(f"• **Chunk #{src['chunk_id'] + 1}** (Relevance Score: {src['score']}):")
                        st.write(f"\"{src['text']}\"")
            st.markdown("---")
