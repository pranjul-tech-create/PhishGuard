import pandas as pd
from url_analyzer import extract_features


# Load original dataset
input_file = "../dataset/PhiUSIIL_Phishing_URL_Dataset.csv"

df = pd.read_csv(input_file)

print("Original dataset shape:", df.shape)


# Keep only URL and label
df = df[["URL", "label"]]


# Remove missing values
df = df.dropna(subset=["URL", "label"])


print("After removing missing values:", df.shape)


# Extract our own features from every URL
print("\nExtracting URL features...")

feature_data = df["URL"].apply(extract_features)

features_df = pd.DataFrame(feature_data.tolist())


# Add the label
features_df["label"] = df["label"].values


# Save processed dataset
output_file = "../dataset/processed_dataset.csv"

features_df.to_csv(output_file, index=False)


print("\nFeature extraction completed!")

print("Processed dataset shape:", features_df.shape)

print("\nFeatures used:")
print(features_df.columns.tolist())

print("\nFirst 5 rows:")
print(features_df.head())

print("\nSaved to:")
print(output_file)