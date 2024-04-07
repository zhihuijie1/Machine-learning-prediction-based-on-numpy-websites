import mysql.connector
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score

# Connect to database
db = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="chengcheng",
    password="171612cgj",
    database="db"
)
print("Connected to database---ok")

# Read data
cursor = db.cursor()
query = "SELECT id, title, description, change_category FROM git_log"
cursor.execute(query)
data = cursor.fetchall()
cursor.close()

# Convert data to pandas DataFrame
df = pd.DataFrame(data, columns=['id', 'title', 'description', 'change_category'])
print("Data read---ok")

# Preprocess and clean data
df['change_category'].fillna(-1, inplace=True)
df = df[df['change_category'] != '']
df['cleaned_title'] = df['title'].str.replace(r"[^a-zA-Z\s]", '', regex=True).str.lower()
df['cleaned_description'] = df['description'].str.replace(r"[^a-zA-Z\s]", '', regex=True).str.lower()
df['combined_text'] = df['cleaned_title'] + " " + df['cleaned_description']
print("Data cleaning and combination---ok")

# Remove stopwords using SpaCy
nlp = spacy.load('en_core_web_sm')
df['combined_text'] = df['combined_text'].apply(lambda x: ' '.join([word for word in x.split() if word not in STOP_WORDS]))
print("Stopwords removed using SpaCy---ok")

# Feature engineering with TF-IDF
vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 2), stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df['combined_text'])
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())
print("Feature engineering---ok")

# Define features and target variable
X = tfidf_df
y = df['change_category'].astype(int)

# Train model
classifier = MultinomialNB()
classifier.fit(X, y)
print("Model trained---ok")

# Predict on the same data (for illustration, usually you should predict on a separate test set)
y_pred = classifier.predict(X)

# Evaluate model
accuracy = accuracy_score(y, y_pred)
recall = recall_score(y, y_pred, average='micro')
precision = precision_score(y, y_pred, average='micro')
f1 = f1_score(y, y_pred, average='micro')

print(f"Accuracy: {accuracy}")
print(f"Recall: {recall}")
print(f"Precision: {precision}")
print(f"F1 Score: {f1}")

# Close database connection
db.close()
print("Database connection closed---ok")
