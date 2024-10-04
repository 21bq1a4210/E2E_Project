import cv2
import numpy as np
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from keras_facenet import FaceNet
from mtcnn.mtcnn import MTCNN
from sklearn.preprocessing import normalize
from .models import FaceRegistration, Attendance
from django.core.files.base import ContentFile
import base64
from scipy.spatial.distance import cosine
from django.shortcuts import render
import json



# Importing the functions from register.py
embedder = FaceNet()
detector = MTCNN()

# Preprocess the image for FaceNet (FaceNet requires 160x160 input size)
def preprocess_image(image):
    img = cv2.resize(image, (160, 160))  # FaceNet uses 160x160 input size
    return np.expand_dims(img, axis=0)

@login_required
def face_recognition_page(request):
    # Render the page for face recognition (e.g., a template with the webcam input)
    return render(request, 'face-1.html')


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

# Decode the base64 image
def decode_base64_image(data):
    data = data.split(',')[1]
    return cv2.imdecode(np.frombuffer(base64.b64decode(data), np.uint8), cv2.IMREAD_COLOR)

# Register a student's face
# Helper function to decode base64 image
def decode_base64_image(image_data):
    image_data = image_data.split(',')[1]  # Remove base64 header
    image_data = base64.b64decode(image_data)
    np_img = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    return img

@csrf_exempt
@login_required
def register_face(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Check if the image data is None
        if 'image' not in data:
            return JsonResponse({'error': 'No image data provided.'}, status=400)

        try:
            image = decode_base64_image(data['image'])
        except Exception as e:
            return JsonResponse({'error': f'Failed to decode image: {str(e)}'}, status=400)

        # Detect face and extract features
        face = detect_face(image)
        if face is not None:
            features = extract_features(face)

            # Save the face image and features in the database for the user
            face_registration, created = FaceRegistration.objects.get_or_create(user=request.user)
            face_registration.face_features = features.tobytes()  # Store features in binary format

            # Store the image in the database
            _, buffer = cv2.imencode('.jpg', face)
            image_data = ContentFile(buffer.tobytes(), name=f'{request.user.username}_face.jpg')
            face_registration.face_image.save(f'{request.user.username}_face.jpg', image_data)

            face_registration.save()
            return JsonResponse({'message': 'Face registered successfully'})
        else:
            return JsonResponse({'message': 'No face detected. Please try again.'})

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@login_required
def check_registration(request):
    if request.method == 'GET':
        # Check if the user has registered a face
        face_registration = FaceRegistration.objects.filter(user=request.user).first()
        is_registered = face_registration is not None and face_registration.face_features is not None
        return JsonResponse({'is_registered': is_registered})

# Recognize face and mark attendance
@csrf_exempt
@login_required
def mark_attendance(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Properly load the JSON body
            image_data = data.get('image')  # Extract image data from JSON

            # Check if the image data is None
            if not image_data:
                return JsonResponse({'error': 'No image data provided.'}, status=400)

            # Decode base64 image
            try:
                image = decode_base64_image(image_data)
            except Exception as e:
                return JsonResponse({'error': f'Failed to decode image: {str(e)}'}, status=400)

            # Detect face and extract features
            face = detect_face(image)
            if face is not None:
                test_features = extract_features(face)

                # Check if the user has a registered face
                face_registration = FaceRegistration.objects.filter(user=request.user).first()

                if face_registration and face_registration.face_features:
                    registered_features = np.frombuffer(face_registration.face_features, dtype=np.float32)

                    # Compare the features using cosine similarity
                    similarity = 1 - cosine(registered_features, test_features)

                    if similarity > 0.60:  # Adjust threshold based on testing
                        # Check if attendance is already marked for today
                        today = timezone.now().date()
                        attendance, created = Attendance.objects.get_or_create(user=request.user, date=today)

                        if created:
                            attendance.status = 'Present'
                            attendance.save()
                            return JsonResponse({'message': 'Attendance marked successfully'})
                        else:
                            return JsonResponse({'message': 'Attendance already marked for today.'})
                    else:
                        return JsonResponse({'message': 'Face not recognized. Please try again.'})
                else:
                    return JsonResponse({'message': 'Face not registered. Please register first.'})
            else:
                return JsonResponse({'message': 'No face detected. Please try again.'})
        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Invalid JSON data: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)