import sys
from pathlib import Path

# Add project root to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

import streamlit as st    
import pandas as pd
import joblib
import io
from config import MODELS_DIR

# Load model + vectorizer using config paths
model = joblib.load(MODELS_DIR / "essay_detector.pkl")
vectorizer = joblib.load(MODELS_DIR / "tfidf_vectorizer.pkl")

# App title
st.title("📝 AI Essay Detector")
st.write("Paste an essay, upload a single `.txt` file, or upload multiple files to classify them all!")

# Text input
essay_text = st.text_area("Enter essay text here...", height=200)

# Single file upload
uploaded_file = st.file_uploader("Or upload a single .txt file", type=["txt"], key="single")

if uploaded_file is not None:
    essay_text = uploaded_file.getvalue().decode("utf-8")

# Multi file upload 
uploaded_files = st.file_uploader(
    "Or upload multiple .txt files", type=["txt"], accept_multiple_files=True, key="multi"
)

# Classification 
if st.button("Classify"):
    if uploaded_files:  # batch mode
        results = []
        for file in uploaded_files:
            text = file.getvalue().decode("utf-8") 
            X = vectorizer.transform([text])
            pred = model.predict(X)[0]
            proba = model.predict_proba(X)[0][pred]
            label = "⚠️ AI Generated" if pred == 1 else "🧠 Human Written"
            results.append({
                "Filename": file.name,
                "Prediction": label,
                "Confidence": round(proba, 2)
            })
        
        df = pd.DataFrame(results)
        st.subheader("📊 Batch Results")
        st.dataframe(df)

        # Download as CSV
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="⬇️ Download Results as CSV",
            data=csv_buffer.getvalue(),
            file_name="essay_classification_results.csv",
            mime="text/csv"
        )

    elif essay_text.strip():  
        X = vectorizer.transform([essay_text])
        pred = model.predict(X)[0]
        proba = model.predict_proba(X)[0][pred]

        label = "⚠️ AI Generated" if pred == 1 else "🧠 Human Written"
        st.subheader("Prediction:")
        st.success(f"{label} (Confidence: {round(proba, 2)})")

    else:
        st.warning("Please enter text or upload file(s) before classifying.")
