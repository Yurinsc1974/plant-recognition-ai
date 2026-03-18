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

weights_path       = os.path.join(BASE_DIR, 'model', 'plant_weights.weights.h5')
class_indices_path = os.path.join(BASE_DIR, 'model', 'class_indices.json')
plants_data_path   = os.path.join(BASE_DIR, 'api', 'plants_data.json')

def build_model(num_classes=5):
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights=None
    )
    model = tf.keras.Sequential([
        base_model,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])
    return model

model = build_model(num_classes=5)
model.build((None, 224, 224, 3))
model.load_weights(weights_path)
print("Modelo carregado com sucesso!")

with open(class_indices_path) as f:
    class_indices = json.load(f)
    idx_to_class = {v: k for k, v in class_indices.items()}

with open(plants_data_path) as f:
    plants_data = json.load(f)

def preprocess_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

@app.post("/identify")
async def identify_plant(file: UploadFile = File(...)):
    image_bytes = await file.read()
    img = preprocess_image(image_bytes)

    predictions = model.predict(img)
    confidence = float(np.max(predictions))
    class_idx = int(np.argmax(predictions))
    plant_name = idx_to_class[class_idx]

    plant_info = plants_data.get(plant_name, {})

    return {
        "planta": plant_name,
        "confianca": f"{confidence * 100:.1f}%",
        "dados": plant_info
    }

@app.get("/health")
def health():
    return {"status": "online"}
