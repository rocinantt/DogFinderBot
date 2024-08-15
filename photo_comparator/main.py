import os
import json
import logging
from datetime import datetime, timedelta
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, List

import asyncpg
import aiohttp
import numpy as np
from fastapi import FastAPI, Request
from pydantic import BaseModel

from config import DATABASE_URL
from model import load_image, extract_features, processor, model  # Импортируем processor и model из model.py
from posts import get_posts
from similarity import calculate_similarity, get_top_n_similar_posts

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the FastAPI application
app = FastAPI()
executor = ThreadPoolExecutor(max_workers=4)

class ImageRequest(BaseModel):
    image_url: str
    region: str
    days: int
    area: Optional[str] = None
    district: Optional[str] = None
    unassigned: bool = False

async def find_similar_images(image_url: str, region: str, days: int, area: Optional[str] = None,
                              district: Optional[str] = None, unassigned: bool = False):
    """Find similar images in the database."""

    posts = await get_posts(region, days, area, district, unassigned)
    query_image_tensor = await load_image(image_url)
    if query_image_tensor is None:
        return []

    query_features = extract_features(query_image_tensor).squeeze().cpu().numpy()

    similar_posts = get_top_n_similar_posts(query_features,
                                            [(post['post_link'], json.loads(post['features']), post['date']) for post in
                                             posts])

    return [{'post_link': post['post_link'], 'date': post['date']} for post in similar_posts]

@app.post('/compare')
async def compare(request: ImageRequest):
    results = await find_similar_images(
        image_url=request.image_url,
        region=request.region,
        days=request.days,
        area=request.area,
        district=request.district,
        unassigned=request.unassigned
    )
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)