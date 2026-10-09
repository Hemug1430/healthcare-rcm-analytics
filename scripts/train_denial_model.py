import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score

# 1. Load the generated synthetic dataset
print("Loading dataset...")
df = pd.read_csv('data/synthetic_rcm_claims.csv')

# 2. Define Target Variable (1 = Denied, 0 = Paid or Pending)
df['Is_Denied'] = df['Status'].apply(lambda x: 1 if x == 'Denied' else 0)

# 3. Encode Categorical Payer Column into Numeric Values
le_payer = LabelEncoder()
df['Payer_Code'] = le_payer.fit_transform(df['Payer'])

# 4. Define Features (X) and Target (y)
X = df[['Payer_Code', 'Billed_Amount']]
y = df['Is_Denied']

# 5. Split Data into 80% Training and 20% Testing Sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 6. Train Random Forest Classifier
print("Training Random Forest Denial Model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 7. Evaluate Model Performance on Unseen Test Data
y_pred = model.predict(X_test)

print("\n==================================================")
print("   HEALTHCARE RCM CLAIM DENIAL MODEL RESULTS     ")
print("==================================================")
print(f"Overall Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%\n")
print("Detailed Performance Report:")
print(classification_report(y_test, y_pred, target_names=['Paid/Pending', 'Denied']))