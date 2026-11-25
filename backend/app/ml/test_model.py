
import joblib

# Load the already trained model
model = joblib.load("models/scamlens_model.pkl")

# New messages that were not used in training
test_messages = [
    "Congratulations! You have won a free prize. Claim it now.",
    "Your bank account will be blocked. Verify your OTP immediately.",
    "Hey, are we meeting for lunch tomorrow?",
    "URGENT! You have won a cash reward. Click here to claim.",
    "Please call me when you reach home.",
    "FREE entry in our weekly competition. Text WIN to 80085."
]

print("\n===== ScamLens ML Predictions =====\n")

for message in test_messages:

    prediction = model.predict([message])[0]

    probabilities = model.predict_proba([message])[0]

    spam_index = list(model.classes_).index("spam")
    spam_probability = probabilities[spam_index] * 100

    if prediction == "spam":
        result = "SPAM"
    else:
        result = "LEGITIMATE"

    print("Message:", message)
    print("Prediction:", result)
    print(f"Spam probability: {spam_probability:.2f}%")
    print("-" * 60)
