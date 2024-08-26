import os
import logging
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, List

import asyncpg
import aiohttp
import ujson as json
import numpy as np
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel

from posts import get_posts
from config import DATABASE_URL, logger
from model import load_image, extract_features
from similarity import get_top_n_similar_posts


# Инициализация FastAPI приложения
app = FastAPI()
executor = ThreadPoolExecutor(max_workers=4)

class ImageRequest(BaseModel):
    image_url: str
    region: str
    days: int
    animal_type: str
    area: Optional[str] = None
    district: Optional[str] = None
    unassigned: bool = False


async def find_similar_images(image_url: str, region: str, days: int, animal_type: str,
                              area: Optional[str] = None, district: Optional[str] = None,
                              unassigned: bool = False):
    """
    Находит похожие изображения в базе данных.

    :param image_url: URL изображения для поиска
    :param region: регион поиска
    :param days: количество дней для поиска
    :param animal_type: тип животного (собака или кошка)
    :param area: область поиска (опционально)
    :param district: район поиска (опционально)
    :param unassigned: флаг, указывающий на нераспределенные области (по умолчанию False)
    :return: список похожих постов
    :rtype: List[dict]
    """

    try:
        posts = await get_posts(region, days, animal_type, area, district, unassigned)
        logger.info(f"Количество найденных постов: {len(posts)}")

        query_image_tensor = await load_image(image_url)
        if query_image_tensor is None:
            logger.error("Не удалось загрузить изображение для сравнения.")
            return []

        query_features = extract_features(query_image_tensor).squeeze().cpu().numpy()
        similar_posts = get_top_n_similar_posts(
            query_features,
            [(post['post_link'], json.loads(post['features']), post['date']) for post in posts]
        )
        logger.info(f"Количество найденных похожих постов: {len(similar_posts)}")

        return similar_posts
    except Exception as e:
        logger.error(f"Ошибка при поиске похожих изображений: {e}")
        raise HTTPException(status_code=500, detail="Произошла ошибка при обработке запроса.")


@app.post('/compare')
async def compare(request: ImageRequest):
    """
    Эндпоинт для сравнения изображений.

    :param request: запрос с параметрами изображения и фильтрации
    :return: список найденных похожих изображений
    """
    results = await find_similar_images(
        image_url=request.image_url,
        region=request.region,
        days=request.days,
        animal_type=request.animal_type,
        area=request.area,
        district=request.district,
        unassigned=request.unassigned
    )
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)