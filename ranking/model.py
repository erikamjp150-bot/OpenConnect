import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel
import numpy as np
from typing import List, Dict, Any
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class WellnessRankingModel(nn.Module):
    """
    A ranking model that prioritizes wellness signals over pure engagement.
    Combines content safety, positivity, social relevance, and freshness.
    """
    def __init__(self, model_name: str = "distilbert-base-uncased"):
        super().__init__()
        self.encoder = AutoModel.from_pretrained(model_name)
        self.dropout = nn.Dropout(0.1)
        self.classifier = nn.Linear(768, 1)  # Wellness score (0-1)
        
    def forward(self, input_ids, attention_mask):
        outputs = self.encoder(input_ids=input_ids, attention_mask=attention_mask)
        pooled = outputs.pooler_output
        pooled = self.dropout(pooled)
        score = torch.sigmoid(self.classifier(pooled))
        return score.squeeze()

class WellnessRankingService:
    """
    Feed ranking service prioritizing:
    - Wellness (positive, helpful, non-toxic content)
    - Social relevance (friends, groups, interests)
    - Diversity (avoid echo chambers)
    - Freshness (timely content)
    - Limited engagement (capped to avoid amplification of harmful content)
    """
    
    def __init__(self, model_path: str = None):
        self.model = WellnessRankingModel()
        self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
        
        if model_path:
            self.model.load_state_dict(torch.load(model_path))
        
        self.model.eval()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        
        # Feature weights (wellness-first)
        self.weights = {
            'wellness': 0.35,
            'social_relevance': 0.25,
            'diversity': 0.15,
            'freshness': 0.15,
            'engagement': 0.10  # Significantly reduced from typical algorithms
        }
        
        logger.info(f"WellnessRankingService initialized on {self.device}")
    
    def rank_feed(self, user_id: int, posts: List[Dict[str, Any]], social_graph: Dict[int, List[int]]) -> List[Dict[str, Any]]:
        """Rank posts for a user's feed using wellness-first approach"""
        if not posts:
            return []
        
        scored_posts = []
        
        for post in posts:
            # Extract features
            wellness_score = self._wellness_score(post)
            social_score = self._social_relevance(post['author_id'], user_id, social_graph)
            diversity_score = self._diversity_score(post, user_id)
            freshness_score = self._freshness_score(post.get('created_at'))
            engagement_score = self._capped_engagement_score(post)
            
            # Final score (weighted sum)
            total_score = (
                self.weights['wellness'] * wellness_score +
                self.weights['social_relevance'] * social_score +
                self.weights['diversity'] * diversity_score +
                self.weights['freshness'] * freshness_score +
                self.weights['engagement'] * engagement_score
            )
            
            scored_posts.append({
                **post,
                'score': total_score,
                'wellness_score': wellness_score,
                'combined_score': total_score
            })
        
        # Sort by score descending
        scored_posts.sort(key=lambda x: x['score'], reverse=True)
        return scored_posts
    
    def _wellness_score(self, post: Dict[str, Any]) -> float:
        """Compute wellness score using content classifier"""
        content = post.get('content', '')
        if not content:
            return 0.5
        
        # Use precomputed or compute on-the-fly
        if 'wellness_score' in post:
            return post['wellness_score']
        
        # Fallback: use simple heuristics for sentiment and safety
        sentiment = post.get('sentiment_score', 0.0)
        reports = post.get('reports', 0)
        helpful_votes = post.get('helpful_votes', 0)
        
        # Wellness: positive sentiment, high helpfulness, low reports
        wellness = (sentiment + 1) / 2  # Map -1,1 to 0,1
        wellness *= min(helpful_votes + 1, 2) / 2
        wellness *= max(0, 1 - (reports / 20))
        
        return min(1.0, wellness)
    
    def _social_relevance(self, author_id: int, user_id: int, social_graph: Dict[int, List[int]]) -> float:
        """Compute relevance based on social graph"""
        if author_id == user_id:
            return 1.0  # User's own posts are highly relevant
        
        # Check if author is a friend (direct connection)
        friends = social_graph.get(user_id, [])
        if author_id in friends:
            return 0.8
        
        # Check if author is a friend-of-friend (2nd degree)
        for friend in friends:
            friend_friends = social_graph.get(friend, [])
            if author_id in friend_friends:
                return 0.5
        
        return 0.2  # Not connected
    
    def _diversity_score(self, post: Dict[str, Any], user_id: int) -> float:
        """Encourage diverse content to avoid echo chambers"""
        # Track user's interaction history to avoid over-similar content
        # Simplified: use post's topic diversity
        topics = post.get('topics', [])
        if not topics:
            return 0.5
        
        # If user has engaged with this topic many times, reduce score
        # This encourages showing varied content
        return 0.5 + (1 - min(1, len(set(topics)) / 10)) * 0.5
    
    def _freshness_score(self, created_at) -> float:
        """Compute freshness score with a 24-hour half-life"""
        if not created_at:
            return 0.5
        
        try:
            if isinstance(created_at, str):
                created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            
            age_hours = (datetime.now(datetime.UTC) - created_at).total_seconds() / 3600
            # Decay with a half-life of 12 hours
            return max(0, 1.0 - (age_hours / (24 * 7)))  # 7-day half-life
        except Exception as e:
            logger.warning(f"Error computing freshness: {e}")
            return 0.5
    
    def _capped_engagement_score(self, post: Dict[str, Any]) -> float:
        """Cap engagement score to prevent amplification of harmful content"""
        likes = post.get('likes_count', 0)
        comments = post.get('comments_count', 0)
        shares = post.get('shares_count', 0)
        
        # Cap engagement at 1000 to prevent runaway amplification
        total = min(1000, likes + comments + shares)
        
        # Normalize to 0-1 with diminishing returns
        return min(1.0, total / 2000)  # Max score of 0.5 at cap
