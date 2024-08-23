import os
import torch
import aiohttp
from PIL import Image
from io import BytesIO
from transformers import ViTImageProcessor, ViTForImageClassification

from config import logger


# Инициализация модели и процессора
model_path = '/app/models'
processor = ViTImageProcessor.from_pretrained(model_path)
model = ViTForImageClassification.from_pretrained(model_path)
model.classifier = torch.nn.Identity()


async def load_image(url: str):
    """Загружает изображение по URL и подготавливает его для модели."""

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                image = Image.open(BytesIO(await response.read())).convert("RGB")
                inputs = processor(images=image, return_tensors="pt")
                return inputs['pixel_values']
    except aiohttp.ClientError as e:
        logger.error(f"Ошибка загрузки изображения по URL {url}: {e}")
        return None

def extract_features(image_tensors):
    """Извлекает признаки из тензора изображения с помощью модели."""

    try:
        with torch.no_grad():
            outputs = model(image_tensors)
        return outputs.logits
    except Exception as e:
        logger.error(f"Ошибка извлечения признаков из изображения: {e}")
        raise
