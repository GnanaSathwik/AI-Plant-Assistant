import re

import numpy as np
import torch
from PIL import Image
from transformers import AutoModelForImageClassification


MODEL_NAME = "linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification"
IMAGE_SIZE = (224, 224)
IMAGENET_MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
IMAGENET_STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)

_model = None


def load_classifier():
    """Load and cache the Hugging Face image classification model."""
    global _model

    if _model is None:
        _model = AutoModelForImageClassification.from_pretrained(MODEL_NAME, use_safetensors=False)
        _model.eval()

    return _model


def preprocess_image(image: Image.Image) -> torch.Tensor:
    """Apply standard MobileNet/ImageNet preprocessing without torchvision."""
    resized_image = image.convert("RGB").resize(IMAGE_SIZE)
    image_array = np.asarray(resized_image, dtype=np.float32) / 255.0
    image_array = (image_array - IMAGENET_MEAN) / IMAGENET_STD
    image_array = np.transpose(image_array, (2, 0, 1))
    return torch.from_numpy(image_array).unsqueeze(0)


def clean_label(label: str) -> str:
    """Convert labels like Tomato___Early_blight into Early Blight."""
    disease = str(label).split("___")[-1]
    disease = disease.replace("_", " ").replace("-", " ")
    disease = re.sub(r"\s+", " ", disease).strip()

    replacements = {
        "healthy": "Healthy",
        "bacterial spot": "Bacterial Spot",
        "black rot": "Black Rot",
        "cedar apple rust": "Cedar Apple Rust",
        "early blight": "Early Blight",
        "late blight": "Late Blight",
        "leaf mold": "Leaf Mold",
        "leaf scorch": "Leaf Scorch",
        "powdery mildew": "Powdery Mildew",
        "septoria leaf spot": "Septoria Leaf Spot",
        "spider mites two spotted spider mite": "Spider Mites Two-Spotted Spider Mite",
        "target spot": "Target Spot",
        "tomato mosaic virus": "Tomato Mosaic Virus",
        "tomato yellow leaf curl virus": "Tomato Yellow Leaf Curl Virus",
    }

    return replacements.get(disease.lower(), disease.title())


def clean_plant_name(plant: str) -> str:
    """Normalize plant names from model labels."""
    plant = str(plant).replace("_", " ").replace("-", " ")
    plant = re.sub(r"\s+", " ", plant).strip()
    return plant.title() if plant else "Unknown Plant"


def split_plant_and_disease(label: str) -> tuple[str, str]:
    """Extract plant and disease names from common plant-disease model labels."""
    raw_label = str(label)

    if "___" in raw_label:
        plant, disease = raw_label.split("___", 1)
        return clean_plant_name(plant), clean_label(disease)

    readable = raw_label.replace("_", " ").replace("-", " ")
    readable = re.sub(r"\s+", " ", readable).strip()
    lower_readable = readable.lower()

    if " with " in lower_readable:
        plant, disease = re.split(r"\s+with\s+", readable, maxsplit=1, flags=re.IGNORECASE)
        return clean_plant_name(plant), clean_label(disease)

    if lower_readable.startswith("healthy "):
        plant = re.sub(r"^healthy\s+", "", readable, flags=re.IGNORECASE)
        plant = re.sub(r"\b(leaf|plant|leaves)\b", "", plant, flags=re.IGNORECASE)
        return clean_plant_name(plant), "Healthy"

    known_plants = [
        "apple",
        "blueberry",
        "cherry",
        "corn",
        "grape",
        "orange",
        "peach",
        "pepper",
        "potato",
        "raspberry",
        "soybean",
        "squash",
        "strawberry",
        "tomato",
    ]
    for plant in known_plants:
        if plant in lower_readable:
            return clean_plant_name(plant), clean_label(readable)

    return "Unknown Plant", clean_label(readable)


def build_prediction_payload(
    raw_label: str,
    confidence_percent: float,
    predicted_index: int,
    top_predictions: list[dict],
) -> dict:
    """Create a structured prediction payload for Streamlit and the LLM."""
    plant_name, disease_name = split_plant_and_disease(raw_label)
    return {
        "plant_name": plant_name,
        "disease_name": disease_name,
        "confidence": confidence_percent,
        "raw_label": raw_label,
        "predicted_index": predicted_index,
        "top_predictions": top_predictions,
    }


def predict_disease(image: Image.Image) -> dict:
    """Return structured plant, disease, confidence, and model metadata."""
    model = load_classifier()
    inputs = preprocess_image(image)

    with torch.no_grad():
        outputs = model(pixel_values=inputs)
        probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)[0]

    predicted_index = int(torch.argmax(probabilities).item())
    confidence_percent = round(float(probabilities[predicted_index].item()) * 100, 2)

    id_to_label = model.config.id2label
    raw_label = id_to_label.get(predicted_index, str(predicted_index))
    top_count = min(5, int(probabilities.numel()))
    top_values, top_indices = torch.topk(probabilities, k=top_count)

    top_predictions = []
    for rank, (score, index) in enumerate(zip(top_values.tolist(), top_indices.tolist()), start=1):
        top_raw_label = id_to_label.get(int(index), str(index))
        top_plant_name, top_disease_name = split_plant_and_disease(top_raw_label)
        top_predictions.append(
            {
                "rank": rank,
                "plant_name": top_plant_name,
                "disease_name": top_disease_name,
                "raw_label": top_raw_label,
                "confidence": round(float(score) * 100, 2),
                "index": int(index),
            }
        )

    return build_prediction_payload(raw_label, confidence_percent, predicted_index, top_predictions)
