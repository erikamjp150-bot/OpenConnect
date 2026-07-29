import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Post from './Post';

const Feed = ({ userToken }) => {
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [page, setPage] = useState(1);

    useEffect(() => {
        fetchFeed();
    }, [page]);

    const fetchFeed = async () => {
        try {
            const response = await axios.get(`${process.env.REACT_APP_API_URL}/feed`, {
                headers: { Authorization: `Bearer ${userToken}` },
                params: { page, page_size: 10 }
            });
            setPosts(prev => [...prev, ...response.data.results]);
            setLoading(false);
        } catch (error) {
            console.error('Error fetching feed:', error);
            setLoading(false);
        }
    };

    const handleLike = async (postId) => {
        try {
            await axios.post(`${process.env.REACT_APP_API_URL}/posts/${postId}/like`, {},
                { headers: { Authorization: `Bearer ${userToken}` } }
            );
            // Update local state
            setPosts(posts.map(post => 
                post.id === postId 
                    ? { ...post, likes_count: post.likes_count + 1, user_liked: true }
                    : post
            ));
        } catch (error) {
            console.error('Error liking post:', error);
        }
    };

    return (
        <div className="feed-container">
            <h2>Your Wellness Feed</h2>
            <div className="feed-explanation">
                <p>This feed prioritizes wellbeing, positivity, and meaningful connections.</p>
            </div>
            
            {loading && <p>Loading posts...</p>}
            
            <div className="posts-list">
                {posts.map(post => (
                    <Post 
                        key={post.id} 
                        post={post} 
                        onLike={handleLike}
                        onComment={handleComment}
                    />
                ))}
            </div>
            
            {!loading && posts.length === 0 && (
                <p>No posts yet. Follow friends to see their updates!</p>
            )}
            
            <button onClick={() => setPage(page + 1)} className="load-more-btn">
                Load More
            </button>
        </div>
    );
};

export default Feed;
