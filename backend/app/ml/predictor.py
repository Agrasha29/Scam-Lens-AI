
from pathlib import Path
import joblib

# Locate the saved ML model
MODEL_PATH = (
    Path(__file__).resolve().parents[2]
    / "models"
    / "scamlens_model.pkl"
)

# Load the trained model only once
model = joblib.load(MODEL_PATH)


def predict_message(message: str):
    """
    Predict whether a message is spam or legitimate.
    Returns the prediction and spam probability.
    """

    if not message or not message.strip():
        raise ValueError("Message cannot be empty.")

    # Predict message category
    prediction = model.predict([message])[0]

    # Get prediction probabilities
    probabilities = model.predict_proba([message])[0]

    # Find spam probability
    spam_index = list(model.classes_).index("spam")
    spam_probability = probabilities[spam_index] * 100

    return {
        "prediction": prediction,
        "spam_probability": round(float(spam_probability), 2)
    }
