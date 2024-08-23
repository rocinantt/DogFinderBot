import os
import requests
from PIL import Image
import torch
from transformers import ViTImageProcessor, ViTForImageClassification
from config import logger

# Загрузка модели и процессора
model_path = '/app/models'
processor = ViTImageProcessor.from_pretrained(model_path)
model = ViTForImageClassification.from_pretrained(model_path)

# Настройка модели для использования только экстрактора признаков
model.classifier = torch.nn.Identity()

def load_image(url):
    """
    Загружает изображение по URL и выполняет предварительную обработку.

    :param url: URL изображения
    :return: тензор изображения
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        image = Image.open(response.raw).convert("RGB")
        inputs = processor(images=image, return_tensors="pt")
        return inputs['pixel_values']
    except requests.RequestException as e:
        logger.error(f"Ошибка при загрузке изображения по URL {url}: {e}")
        raise
    except Exception as e:
        logger.error(f"Ошибка при обработке изображения: {e}")
        raise

def extract_features_batch(image_tensors):
    """
    Извлекает признаки из батча тензоров изображений.

    :param image_tensors: тензоры изображений
    :return: логиты (признаки изображений)
    """
    try:
        with torch.no_grad():
            outputs = model(image_tensors)
        return outputs.logits
    except Exception as e:
        logger.error(f"Ошибка при извлечении признаков из изображений: {e}")
        raise

def process_post(post):
    """
    Обрабатывает пост для извлечения признаков изображений.

    :param post: пост с изображениями
    :return: список признаков изображений
    """
    post_features = []
    try:
        for photo_url in post['photos']:
            image_tensor = load_image(photo_url)
            if image_tensor is None:
                logger.error(f"Пропуск изображения по URL {photo_url} из-за ошибки загрузки.")
                continue
            features = extract_features_batch(image_tensor).squeeze().cpu().tolist()
            if len(features) == 0:
                logger.error(f"Пропуск изображения по URL {photo_url} из-за ошибки извлечения признаков.")
                continue
            post_features.append(features)
        return post_features
    except Exception as e:
        logger.error(f"Ошибка при обработке поста {post['post_id']}: {e}")
        return []
