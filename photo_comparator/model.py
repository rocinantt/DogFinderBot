import os
import torch
import aiohttp
import logging
from PIL import Image
from io import BytesIO
from transformers import AutoImageProcessor, AutoModelForImageClassification

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize model and processor
model_path = '/app/models'
processor = AutoImageProcessor.from_pretrained(model_path)
model = AutoModelForImageClassification.from_pretrained(model_path)
model.classifier = torch.nn.Identity()

async def load_image(url: str):
    """Load an image from a URL."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                image = Image.open(BytesIO(await response.read())).convert("RGB")
                inputs = processor(images=image, return_tensors="pt")
                return inputs['pixel_values']
    except aiohttp.ClientError as e:
        logger.error(f"Error loading image from URL {url}: {e}")
        return None

def extract_features(image_tensors):
    """Extract features from an image tensor."""
    with torch.no_grad():
        outputs = model(image_tensors)
    return outputs.logits
