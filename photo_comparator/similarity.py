import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import heapq


def calculate_similarity(query_features, post_features):
    """Calculate the cosine similarity between query features and post features."""
    post_features = np.array(post_features)
    # Вычисление сходства сразу для всех постов, а не построчно
    similarities = cosine_similarity([query_features], post_features)[0]
    return similarities


def get_top_n_similar_posts(query_features, posts, n=5):
    """Get the top N similar posts based on similarity scores."""
    post_features = [post[1] for post in posts]  # Извлекаем признаки постов
    similarities = calculate_similarity(query_features, post_features)

    # Создаем список кортежей (сходство, ссылка на пост, дата поста)
    posts_with_similarity = [(similarity, post[0], post[2]) for post, similarity in zip(posts, similarities)]

    # Используем heapq для получения топ-N постов с наивысшим сходством
    similar_posts = heapq.nlargest(n, posts_with_similarity, key=lambda x: x[0])

    # Возвращаем топ-N постов с схожестью, ссылкой на пост и датой
    return [{'post_link': post_link, 'similarity': similarity, 'date': post_date.strftime('%d-%m-%Y')}
            for similarity, post_link, post_date in similar_posts]
