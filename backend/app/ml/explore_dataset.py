
import pandas as pd

# Dataset location
DATASET_PATH = "data/SMSSpamCollection"

# Load dataset
df = pd.read_csv(
    DATASET_PATH,
    sep="\t",
    header=None,
    names=["label", "message"],
    encoding="utf-8"
)

# Display first 5 messages
print("\n--- First 5 Messages ---")
print(df.head())

# Dataset information
print("\n--- Dataset Information ---")
print(df.info())

# Count spam and legitimate messages
print("\n--- Label Distribution ---")
print(df["label"].value_counts())

# Check missing values
print("\n--- Missing Values ---")
print(df.isnull().sum())

# Dataset size
print("\n--- Dataset Shape ---")
print(df.shape)
