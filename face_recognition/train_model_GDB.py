# import the necessary packages
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import argparse
import pickle

# load the face embeddings
print("[INFO] loading face embeddings...")
data = pickle.loads(open("output/embeddings_test.pickle", "rb").read())

# encode the labels
print("[INFO] encoding labels...")
le = LabelEncoder()
labels = le.fit_transform(data["names"])

# train the model used to accept the 128-d embeddings of the face and
# then produce the actual face recognition
print("[INFO] training model...")
# Change the classifier here to GradientBoostingClassifier.
classifier = GradientBoostingClassifier()

classifier.fit(data["embeddings"], labels)

# predict labels for the training set
predictions = classifier.predict(data["embeddings"])

# calculate accuracy
accuracy = accuracy_score(labels, predictions)
print(f"[INFO] Accuracy: {accuracy * 100:.2f}%")

# calculate and display other performance metrics
print("[INFO] Classification Report:")
print(classification_report(labels, predictions, target_names=le.classes_))

print("[INFO] Confusion Matrix:")
print(confusion_matrix(labels, predictions))

# write the actual face recognition model to disk
f = open("output/recognizer_gbc.pickle", "wb")  # Changed filename for GBC
f.write(pickle.dumps(classifier))
f.close()

# write the label encoder to disk
f = open("output/le.pickle", "wb")
f.write(pickle.dumps(le))
f.close()

print("done..")

