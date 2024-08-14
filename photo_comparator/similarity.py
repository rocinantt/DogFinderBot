import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import heapq

def calculate_similarity(query_features, post_features):
    """Calculate the cosine similarity between query features and post features."""
    post_features = np.array(post_features)
    similarities = cosine_similarity([query_features], post_features)[0]
    max_similarity = np.max(similarities)
    return max_similarity

def get_top_n_similar_posts(query_features, posts, n=5):
    """Get the top N similar posts based on similarity scores."""
    similarities = []
    for post in posts:
        similarity = calculate_similarity(query_features, post[1])
        similarities.append(similarity)
    
    # Create a list of (similarity, post_link, post_date) tuples
    posts_with_similarity = [(similarity, post[0], post[2]) for post, similarity in zip(posts, similarities)]
    
    # Use heapq to get the top N posts with highest similarity
    similar_posts = heapq.nlargest(n, posts_with_similarity, key=lambda x: x[0])
    
    # Return the top N posts with similarity, post link, and date
    return [{'post_link': post_link, 'similarity': similarity, 'date': post_date.strftime('%d-%m-%Y')} 
            for similarity, post_link, post_date in similar_posts]
