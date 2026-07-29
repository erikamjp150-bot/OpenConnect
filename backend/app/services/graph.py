from neo4j import GraphDatabase
from typing import List, Dict, Any
from ..config import settings
import logging

logger = logging.getLogger(__name__)

class GraphService:
    """Service for interacting with the social graph (Neo4j)"""
    
    def __init__(self):
        self.driver = GraphDatabase.driver(
            settings.NEO4J_URL,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )
    
    def close(self):
        self.driver.close()
    
    def add_friend(self, user_id: int, friend_id: int) -> bool:
        """Add a friendship relationship between two users"""
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (u:User {id: $user_id})
                MATCH (f:User {id: $friend_id})
                CREATE (u)-[:FRIENDS_WITH {created_at: datetime()}]->(f)
                CREATE (f)-[:FRIENDS_WITH {created_at: datetime()}]->(u)
                RETURN u, f
                """,
                user_id=user_id,
                friend_id=friend_id
            )
            return result.single() is not None
    
    def get_friends(self, user_id: int) -> List[int]:
        """Get all friends of a user"""
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (u:User {id: $user_id})-[:FRIENDS_WITH]-(f:User)
                RETURN f.id AS friend_id
                """,
                user_id=user_id
            )
            return [record['friend_id'] for record in result]
    
    def get_friends_of_friends(self, user_id: int) -> List[int]:
        """Get friends-of-friends (2nd degree connections)"""
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (u:User {id: $user_id})-[:FRIENDS_WITH]-(f:User)-[:FRIENDS_WITH]-(fof:User)
                WHERE fof.id <> $user_id
                RETURN DISTINCT fof.id AS friend_id
                """,
                user_id=user_id
            )
            return [record['friend_id'] for record in result]
    
    def recommend_friends(self, user_id: int) -> List[Dict[str, Any]]:
        """Recommend friends using graph algorithms"""
        with self.driver.session() as session:
            result = session.run(
                """
                // Common friends recommendation
                MATCH (u:User {id: $user_id})
                MATCH (u)-[:FRIENDS_WITH]-(common:User)-[:FRIENDS_WITH]-(recommended:User)
                WHERE NOT (u)-[:FRIENDS_WITH]-(recommended)
                AND u.id <> recommended.id
                RETURN recommended.id AS user_id, COUNT(common) AS common_friends
                ORDER BY common_friends DESC
                LIMIT 20
                """,
                user_id=user_id
            )
            return [{'user_id': record['user_id'], 'score': record['common_friends']} for record in result]
