
from app.ml.predictor import predict_message

messages = [
    "Congratulations! You won a free prize. Claim now.",
    "Your bank account will be blocked. Verify your OTP immediately.",
    "Hey, are we meeting for lunch tomorrow?"
]

for message in messages:

    result = predict_message(message)

    print("\nMessage:", message)
    print("ML Prediction:", result["prediction"])
    print("Spam Probability:", result["spam_probability"], "%")
    print("-" * 50)
