import Header from '../components/common/header'
import PostList from '../components/post/posts'
import { useState } from 'react';
import { Post } from '../components/post/posts';
import { useSelector } from 'react-redux';
import { selectTokenExists, selectCurrentUser } from '../features/auth/authSlice';


const HomePage = () => {
   const [posts, setPosts] = useState<Post[]>([]); 
   const [postRatings, setPostRatings] = useState<{ postId: number; userId: number; like: boolean; dislike: boolean; }[]>([]);
   const tokenExists = useSelector(selectTokenExists);
   const userId = useSelector(selectCurrentUser)
   const [err, setErr] = useState(false);

    const handlePostsError = () => {
      setErr(true);
    };

  return (
    <>
      <Header/>
      <PostList posts={posts} err={err} handlePostsError={handlePostsError} postRatings={postRatings} setPosts={setPosts} setPostRatings={setPostRatings} tokenExists={tokenExists} auth_user_id={userId} sortById={false} idToSort={null} />
    </>
  );
};

export default HomePage;