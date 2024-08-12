import os
import json
import logging
from datetime import datetime, timedelta
from io import BytesIO

import torch
import asyncpg
import aiohttp
import numpy as np
from PIL import Image
from fastapi import FastAPI, Request
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, List
from transformers import AutoImageProcessor, AutoModelForImageClassification
from sklearn.metrics.pairwise import cosine_similarity

from config import DATABASE_URL
from model import load_image, extract_features
from posts import get_posts
from similarity import calculate_similarity, get_top_n_similar_posts

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the FastAPI application
app = FastAPI()
executor = ThreadPoolExecutor(max_workers=4)

# Initialize model and processor
model_path = '/app/models'
processor = AutoImageProcessor.from_pretrained(model_path)
model = AutoModelForImageClassification.from_pretrained(model_path)
model.classifier = torch.nn.Identity()

class ImageRequest(BaseModel):
    """Request model for image comparison endpoint."""
    image_url: str
    region: str
    days: int
    city: Optional[str] = None

async def find_similar_images(image_url: str, region: str, days: int, city: Optional[str] = None):
    """Find similar images in the database."""
    
    # Fetch posts from the database
    posts = await get_posts(region, days, city)
    
    # Load and process the query image
    query_image_tensor = await load_image(image_url)
    if query_image_tensor is None:
        return []

    query_features = extract_features(query_image_tensor).squeeze().cpu().numpy()
    
    # Calculate similarity with database images
    similar_posts = get_top_n_similar_posts(query_features, [(post['post_link'], json.loads(post['features']), post['date']) for post in posts])
    
    return [{'post_link': post['post_link'], 'date': post['date']} for post in similar_posts]

@app.post('/compare')
async def compare(request: ImageRequest):
    """Endpoint for comparing images."""
    results = await find_similar_images(request.image_url, request.region, request.days, request.city)
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)
