import os
import requests
import numpy as np
from PIL import Image
import torch
from sklearn.preprocessing import normalize
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


def normalize_features(features):
    """
    Нормализует векторы признаков.

    :param features: векторы признаков
    :return: нормализованные векторы признаков
    """
    return normalize(features, axis=1)


def process_post(post):
    """
    Обрабатывает пост для извлечения признаков изображений.

    :param post: пост с изображениями
    :return: список нормализованных признаков изображений
    """
    post_features = []
    image_tensors_list = []

    try:
        # Загрузка всех изображений и сбор в один батч
        for photo_url in post['photos']:
            image_tensor = load_image(photo_url)
            if image_tensor is None:
                logger.error(f"Пропуск изображения по URL {photo_url} из-за ошибки загрузки.")
                continue
            image_tensors_list.append(image_tensor)

        if len(image_tensors_list) == 0:
            logger.error(f"Все изображения в посте {post['post_id']} не удалось загрузить.")
            return []

        # Объединяем все тензоры в один батч
        image_tensors_batch = torch.cat(image_tensors_list, dim=0)

        # Извлекаем признаки сразу для всего батча
        features_batch = extract_features_batch(image_tensors_batch).cpu().numpy()

        # Нормализуем все признаки в батче
        normalized_features_batch = normalize_features(features_batch)

        # Сохраняем нормализованные признаки для каждого изображения
        for normalized_features in normalized_features_batch:
            post_features.append(normalized_features.tolist())

        return post_features
    except Exception as e:
        logger.error(f"Ошибка при обработке поста {post['post_id']}: {e}")
        return []
