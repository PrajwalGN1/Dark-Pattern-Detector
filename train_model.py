import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
import pickle

# 1. Create a "Dummy" Dataset
# In a real project, you would have thousands of rows in a CSV file.
data = {
    'text': [
        "Hurry! Only 2 items left in stock!",      # Dark Pattern (Urgency)
        "15 people are looking at this right now", # Dark Pattern (Social Proof)
        "Offer expires in 10 minutes!",            # Dark Pattern (Urgency)
        "Sign up to get 10% off",                  # Normal Marketing
        "Free shipping on orders over $50",        # Normal Marketing
        "Add to cart",                             # Normal UI
        "Limited time offer!",                     # Dark Pattern
        "This product is eco-friendly",            # Normal Info
        "Don't miss out! Buy now!",                # Dark Pattern
        "Contact us for more details"              # Normal Info
    ],
    'label': [1, 1, 1, 0, 0, 0, 1, 0, 1, 0] # 1 = Dark Pattern, 0 = Safe
}

df = pd.read_csv("DarkPattern.csv") 
# If you had a CSV, you'd use this.
#df = pd.DataFrame(data)

# 2. Convert Text to Numbers (Vectorization)
# Computers can't read words, so we turn words into a matrix of numbers.
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['text'])
y = df['label']

# 3. Train the Model
# We use Random Forest because it's great for classification.
model = RandomForestClassifier()
model.fit(X, y)

# 4. Save the "Brain"
# We save the model and vectorizer so we can use them in the next script.
with open("dark_pattern_model.pkl", "wb") as f:
    pickle.dump(model, f)
with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("✅ Model trained and saved successfully!")
