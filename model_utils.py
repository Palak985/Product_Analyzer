# model_utils.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import pickle
import os

# Define file paths for the model and vectorizer
MODEL_PATH = 'sentiment_model.pkl'
VECTORIZER_PATH = 'tfidf_vectorizer.pkl'

def train_and_save_model():
    """
    Trains a Logistic Regression model for sentiment analysis and saves it.
    
    NOTE: In a real project, you would replace this small dummy_data 
    with your full Kaggle dataset file (e.g., loaded from data/reviews.csv).
    """
    print("Training new sentiment model...")
    
    # --- DUMMY DATA FOR DEMONSTRATION ---
    # Replace this with loading your actual, labeled Kaggle data
    dummy_data = {
        'review_text': [
            "This product is amazing and worth every penny.",
            "Absolutely terrible quality, a complete waste of money.",
            "It was okay, nothing special, but it works.",
            "Highly recommend, best purchase this year!",
            "Breaks easily, very disappointed with this item."
        ],
        'sentiment': ['Positive', 'Negative', 'Neutral', 'Positive', 'Negative']
    }
    df = pd.DataFrame(dummy_data)
    
    # 1. Define the Machine Learning Pipeline)
    # model_utils.py (New Code)
    sentiment_model = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=5000)),
        # This simpler line will work with the lbfgs solver:
        ('clf', LogisticRegression(solver='lbfgs', max_iter=1000)) 
    ])

    # 2. Train the model
    # Note: We skip the advanced preprocessing here assuming the input text is already cleaned.
    sentiment_model.fit(df['review_text'], df['sentiment'])

    # 3. Save the trained pipeline (model + vectorizer)
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(sentiment_model, f)
        
    print(f"Model saved successfully to {MODEL_PATH}")
    return sentiment_model

def load_or_train_model():
    """Loads the model if it exists, otherwise trains a new one."""
    if os.path.exists(MODEL_PATH):
        print("Loading existing sentiment model...")
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        return model
    else:
        return train_and_save_model()

# Load the model once when the Flask app starts
SENTIMENT_MODEL = load_or_train_model()