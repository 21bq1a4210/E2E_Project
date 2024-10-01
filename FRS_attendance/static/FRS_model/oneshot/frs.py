import cv2
import numpy as np
from keras_facenet import FaceNet
from sklearn.preprocessing import normalize
from scipy.spatial.distance import cosine
from mtcnn.mtcnn import MTCNN  # Import MTCNN for face detection

# Initialize the FaceNet embedder and MTCNN detector
embedder = FaceNet()
detector = MTCNN()

# Preprocess the image for FaceNet (FaceNet requires 160x160 input size)
def preprocess_image(image):
    img = cv2.resize(image, (160, 160))  # FaceNet uses 160x160 input size
    return np.expand_dims(img, axis=0)

# Extract features from an image using FaceNet
def extract_features(img):
    img = preprocess_image(img)
    features = embedder.embeddings(img)
    normalized_features = normalize(features)
    return normalized_features.flatten()

# Detect faces using MTCNN
def detect_face(frame):
    faces = detector.detect_faces(frame)
    if faces:
        x, y, w, h = faces[0]['box']
        return frame[y:y+h, x:x+w]  # Return the first detected face
    return None

# Register a student's face
def register_student():
    cap = cv2.VideoCapture(0)
    print("Press 'q' to capture student's face for registration.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Live Capture", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    face = detect_face(frame)
    if face is not None:
        features = extract_features(face)
        print("Registration complete!")
        return features
    else:
        print("No face detected.")
        return None

# Recognize a face using the webcam
def recognize_face(registered_features):
    cap = cv2.VideoCapture(0)
    print("Press 'q' to capture image for recognition.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Live Recognition Capture", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    face = detect_face(frame)
    if face is not None:
        test_features = extract_features(face)
        similarity = 1 - cosine(registered_features, test_features)

        if similarity > 0.60:  # Adjust threshold based on testing
            print(f"Face recognized with similarity: {similarity:.2f}")
        else:
            print(f"Face not recognized. Similarity: {similarity:.2f}")
    else:
        print("Face not detected in the recognition image.")

# Main execution flow
if __name__ == "__main__":
    # Step 1: Register student's face from webcam
    student_features = register_student()

    # Step 2: Recognize the captured face using the webcam
    if student_features is not None:
        recognize_face(student_features)
