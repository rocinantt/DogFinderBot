import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import heapq


def calculate_similarity(query_features, post_features):
    """Calculate the maximum cosine similarity between query features and post features."""
    # Рассматриваем каждый feature-вектор поста отдельно
    similarities = cosine_similarity([query_features], post_features)
    max_similarity = np.max(similarities)
    return max_similarity


def get_top_n_similar_posts(query_features, posts, n=5):
    """Get the top N similar posts based on similarity scores."""
    similarities = []

    for post in posts:
        post_features = np.array(post[1])
        # Рассчитываем максимальную схожесть для поста (в случае, если есть несколько фотографий)
        max_similarity = calculate_similarity(query_features, post_features)
        similarities.append(max_similarity)

    # Создаем список кортежей (similarity, post_link, post_date)
    posts_with_similarity = [(similarity, post[0], post[2]) for post, similarity in zip(posts, similarities)]

    # Используем heapq для получения N постов с самой высокой схожестью
    similar_posts = heapq.nlargest(n, posts_with_similarity, key=lambda x: x[0])

    # Возвращаем список N наиболее похожих постов
    return [{'post_link': post_link, 'similarity': similarity, 'date': post_date.strftime('%d-%m-%Y')}
            for similarity, post_link, post_date in similar_posts]
