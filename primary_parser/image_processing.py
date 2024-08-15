#image_processing.py
import os
import requests
from PIL import Image
import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification

# Load the model and processor
model_path = '/app/models'
processor = AutoImageProcessor.from_pretrained(model_path)
model = AutoModelForImageClassification.from_pretrained(model_path)

# Configure the model to use only the feature extractor
model.classifier = torch.nn.Identity()

def load_image(url):
    """Load an image from a URL and preprocess it."""
    image = Image.open(requests.get(url, stream=True).raw).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    return inputs['pixel_values']

def extract_features_batch(image_tensors):
    """Extract features from a batch of image tensors."""
    with torch.no_grad():
        outputs = model(image_tensors)
    return outputs.logits

def process_post(post):
    """Process a post to extract image features."""
    post_features = []
    for photo_url in post['photos']:
        image_tensor = load_image(photo_url)
        features = extract_features_batch(image_tensor).squeeze().cpu().tolist()
        post_features.append(features)

    return post_features

