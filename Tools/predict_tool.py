from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import nltk
# nltk.download('punkt')
from sklearn.model_selection import train_test_split
import random

from Tools.voice_dataset import intents

training_data = []
labels = []

for intent , data in intents.items():
    for pattern in data['patterns']:
        training_data.append(pattern.lower())
        labels.append(intent)
Vectorizer = TfidfVectorizer(tokenizer=nltk.word_tokenize,stop_words="english",max_df=0.8,min_df=1)
X_train = Vectorizer.fit_transform(training_data)
X_train,X_test,Y_train,Y_test = train_test_split(X_train,labels,test_size=0.4,random_state=42,stratify=labels)

model = SVC(kernel='linear', probability=True, C=1.0)
model.fit(X_train, Y_train)

# predictions = model.predict(X_test)

def predict_intent(user_input):
    user_input = user_input.lower()
    input_vector = Vectorizer.transform([user_input])
    intent = model.predict(input_vector)[0]
    
    if intent in intents:
        responses = intents[intent]['responses']
        response = random.choice(responses)
    return intent , response