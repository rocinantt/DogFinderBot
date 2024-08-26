import numpy as np
import faiss
from sklearn.preprocessing import normalize
import heapq


# Нормализуем векторы
def normalize_vectors(vectors):
    return normalize(vectors, axis=1)


# Строим Faiss индекс для списка векторов внутри поста
def create_faiss_index_for_post(post_features):
    index = faiss.IndexFlatIP(post_features.shape[1])  # IndexFlatIP для косинусного сходства
    index.add(post_features)
    return index


# Находим самый похожий вектор внутри каждого поста
def get_top_n_similar_posts(query_features, posts, n=50):
    best_similarities = []

    # Нормализуем целевой вектор
    query_features = normalize_vectors(np.array([query_features]))[0]

    for post in posts:
        post_features = np.array(post[1])
        post_features = normalize_vectors(post_features)  # Нормализуем признаки постов

        index = create_faiss_index_for_post(post_features)
        distances, indices = index.search(np.array([query_features]), 1)  # Ищем самый близкий вектор внутри поста

        similarity = distances[0][0]  # В IndexFlatIP similarity = косинусное сходство
        best_similarities.append((similarity, post[0], post[2]))

    # Используем heapq для получения N постов с самой высокой схожестью
    similar_posts = heapq.nlargest(n, best_similarities, key=lambda x: x[0])
    # Сортируем посты
    similar_posts = sorted(similar_posts, key=lambda x: x[0], reverse=True)

    return [{'post_link': post_link, 'date': post_date.strftime('%d-%m-%Y')}
            for _, post_link, post_date in similar_posts]