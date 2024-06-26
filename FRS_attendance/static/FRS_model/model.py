import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.src.applications.resnet import preprocess_input
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import cv2
import os

model_path = 'my_student_model_97.h5'
