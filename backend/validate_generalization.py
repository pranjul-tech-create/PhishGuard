import pandas as pd

from sklearn.model_selection import GroupShuffleSplit
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

from url_analyzer import extract_features


# =========================================================
# STEP 1: LOAD ORIGINAL DATASET
# =========================================================

dataset_path = "../dataset/PhiUSIIL_Phishing_URL_Dataset.csv"

df = pd.read_csv(dataset_path)

print("Original dataset shape:")
print(df.shape)


# =========================================================
# STEP 2: REMOVE MISSING VALUES
# =========================================================

df = df[
    ["URL", "Domain", "label"]
].dropna()

print("\nAfter removing missing values:")
print(df.shape)


# =========================================================
# STEP 3: EXTRACT OUR URL FEATURES
# =========================================================

print("\nExtracting URL features...")

feature_data = df["URL"].apply(
    extract_features
)

features_df = pd.DataFrame(
    feature_data.tolist()
)


# =========================================================
# STEP 4: SEPARATE FEATURES AND LABEL
# =========================================================

X = features_df

y = df["label"]

groups = df["Domain"]


# =========================================================
# STEP 5: GROUPED TRAIN / TEST SPLIT
# =========================================================

splitter = GroupShuffleSplit(
    n_splits=1,
    test_size=0.20,
    random_state=42
)

train_indices, test_indices = next(
    splitter.split(
        X,
        y,
        groups=groups
    )
)


X_train = X.iloc[train_indices]

X_test = X.iloc[test_indices]

y_train = y.iloc[train_indices]

y_test = y.iloc[test_indices]


# =========================================================
# STEP 6: CHECK DOMAIN SEPARATION
# =========================================================

train_domains = set(
    groups.iloc[train_indices]
)

test_domains = set(
    groups.iloc[test_indices]
)

overlap = train_domains.intersection(
    test_domains
)


print("\n" + "=" * 60)
print("GROUPED DATASET SPLIT")
print("=" * 60)

print(
    "Training samples:",
    len(X_train)
)

print(
    "Testing samples:",
    len(X_test)
)

print(
    "Training domains:",
    len(train_domains)
)

print(
    "Testing domains:",
    len(test_domains)
)

print(
    "Domain overlap:",
    len(overlap)
)

print("=" * 60)


# =========================================================
# STEP 7: TRAIN RANDOM FOREST
# =========================================================

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

print("\nTraining grouped model...")

model.fit(
    X_train,
    y_train
)

print("Training completed!")


# =========================================================
# STEP 8: MAKE PREDICTIONS
# =========================================================

y_pred = model.predict(
    X_test
)


# =========================================================
# STEP 9: CALCULATE ACCURACY
# =========================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)


# =========================================================
# STEP 10: DISPLAY RESULTS
# =========================================================

print("\n" + "=" * 60)
print("GENERALIZATION TEST")
print("=" * 60)

print(
    f"\nAccuracy: {accuracy * 100:.2f}%"
)

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred
    )
)

print("\nConfusion Matrix:")

print(
    confusion_matrix(
        y_test,
        y_pred
    )
)

print("\n" + "=" * 60)

print(
    "Domain overlap should be 0."
)

print(
    "This test measures performance on domains "
    "not present in the training set."
)

print("=" * 60)