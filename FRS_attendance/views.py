import json
import base64
import numpy as np
import cv2
import os
import tensorflow as tf
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Attendance

# Load the pre-trained model
model = load_model('FRS_attendance/static/FRS_model/my_student_model_97.h5', compile=False)

# Compile the model with a new optimizer
model.compile(optimizer=tf.keras.optimizers.Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

# Define the class names for your dataset
class_names = ['Akshay Kumar', 'Alexandra Daddario', 'Alia Bhatt', 'Amitabh Bachchan',
               'Andy Samberg', 'Anushka Sharma', 'Billie Eilish', 'Brad Pitt', 'Camila Cabello',
               'Charlize Theron', 'Claire Holt', 'Courtney Cox', 'Dwayne Johnson', 'Elizabeth Olsen',
               'Ellen Degeneres', 'Henry Cavill', 'Hrithik Roshan', 'Hugh Jackman', 'Jessica Alba',
               'Lisa Kudrow', 'Margot Robbie', 'Natalie Portman', 'Priyanka Chopra', 'Robert Downey Jr',
               'Roger Federer', 'Tom Cruise', 'Vijay Deverakonda', 'Virat Kohli', 'Zac Efron', 'komal', 'sri hari']

# Get the directory containing Haar cascade files
cascade_dir = cv2.data.haarcascades

# Path to the Haar cascade file for frontal face detection
cascade_file = os.path.join(cascade_dir, 'haarcascade_frontalface_default.xml')

# Check if the cascade file exists
if not os.path.isfile(cascade_file):
    print("Haar cascade file not found. Downloading...")
    cv2_base_url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/"
    cascade_url = cv2_base_url + 'haarcascade_frontalface_default.xml'
    os.system(f"wget {cascade_url} -P {cascade_dir}")
    print("Haar cascade file downloaded successfully.")

# Now, you can use cascade_file as the filter_path in your code.
filter_path = cascade_file


def load_and_preprocess_image(img_array, target_size):
    """Preprocesses a single image for model prediction."""
    img = cv2.resize(img_array, target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)  # Preprocess image
    return img_array


def detect_and_crop_faces(img_array, filter_path):
    """Detects faces in the image and returns the cropped faces."""
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    face_cascade = cv2.CascadeClassifier(filter_path)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    cropped_faces = [(img_array[y:y + h, x:x + w], (x, y, w, h)) for (x, y, w, h) in faces]
    return cropped_faces, img_array


@csrf_exempt
def predict(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_data = data['image'].split(',')[1]
            image_data = base64.b64decode(image_data)
            np_img = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

            # Detect and crop faces
            cropped_faces, original_img = detect_and_crop_faces(img, filter_path)

            if not cropped_faces:
                return JsonResponse({'message': 'No faces detected'})

            recognized_names = []
            for face, (x, y, w, h) in cropped_faces:
                # Preprocess the cropped face
                img_array = load_and_preprocess_image(face, target_size=(224, 224))

                # Make prediction
                predictions = model.predict(img_array)
                pred_idx = np.argmax(predictions[0])
                predicted_label = class_names[pred_idx]
                recognized_names.append(predicted_label)

            return JsonResponse({'message': 'Face recognized', 'names': recognized_names})

        except json.JSONDecodeError as e:
            return JsonResponse({'message': 'Invalid JSON data', 'error': str(e)})
        except KeyError as e:
            return JsonResponse({'message': 'Key error', 'error': str(e)})
        except Exception as e:
            return JsonResponse({'message': 'An error occurred', 'error': str(e)})

    return JsonResponse({'message': 'Invalid request method'})


def face_recognition(request):
    return render(request, 'face-1.html')