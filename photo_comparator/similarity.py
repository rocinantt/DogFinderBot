import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import heapq
from config import logger


def calculate_similarity(query_features, post_features):
    """
    Рассчитывает максимальную косинусную схожесть между признаками запроса и поста.

    :param query_features: признаки изображения-запроса
    :param post_features: признаки изображения-поста
    :return: максимальная схожесть
    :rtype: float
    """
    try:
        similarities = cosine_similarity([query_features], post_features)
        max_similarity = np.max(similarities)
        return max_similarity
    except Exception as e:
        logger.error(f"Ошибка расчета схожести: {e}")
        raise


def get_top_n_similar_posts(query_features, posts, n=50):
    """
    Получает топ N наиболее похожих постов на основе расчета схожести.

    :param query_features: признаки изображения-запроса
    :param posts: список постов с их признаками и данными
    :param n: количество возвращаемых постов
    :return: список похожих постов
    :rtype: List[dict]
    """
    try:
        similarities = []

        for post in posts:
            post_features = np.array(post[1])
            max_similarity = calculate_similarity(query_features, post_features)
            similarities.append(max_similarity)

        # Создаем список кортежей (similarity, post_link, post_date)
        posts_with_similarity = [(similarity, post[0], post[2]) for post, similarity in zip(posts, similarities)]
        logger.info(f"Количество постов с рассчитанной схожестью: {len(posts_with_similarity)}")

        # Используем heapq для получения N постов с самой высокой схожестью
        similar_posts = heapq.nlargest(n, posts_with_similarity, key=lambda x: x[0])

        # Возвращаем список N наиболее похожих постов
        return [{'post_link': post_link, 'similarity': similarity, 'date': post_date.strftime('%d-%m-%Y')}
                for similarity, post_link, post_date in similar_posts]
    except Exception as e:
        logger.error(f"Ошибка получения похожих постов: {e}")
        raise