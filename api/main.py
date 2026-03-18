from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
import numpy as np
from PIL import Image
import json
import io
import os

app = FastAPI(title="Plant Recognition API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model_path         = os.path.join(BASE_DIR, 'model', 'plant_model.h5')
class_indices_path = os.path.join(BASE_DIR, 'model', 'class_indices.json')
plants_data_path   = os.path.join(BASE_DIR, 'api', 'plants_data.json')

model = tf.keras.models.load_model(model_path)

with open(class_indices_path) as f:
    class_indices = json.load(f)
    idx
