
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
df = pd.read_csv(
    "data/SMSSpamCollection",
    sep="\t",
    header=None,
    names=["label", "message"],
    encoding="utf-8"
)

X = df["message"]
y = df["label"]

# Same train-test split for fair comparison
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Define algorithms
models = {
    "Logistic Regression": LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=42
    ),
    "Multinomial Naive Bayes": MultinomialNB()
}

# Train and compare
for name, classifier in models.items():

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
            max_features=5000
        )),
        ("classifier", classifier)
    ])

    print(f"\n{'=' * 45}")
    print(name)
    print("=" * 45)

    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)

    print(
        "Accuracy:",
        round(accuracy_score(y_test, predictions) * 100, 2),
        "%"
    )

    print("\nClassification Report:")
    print(classification_report(y_test, predictions))
