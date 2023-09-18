import CreatePost from '../components/post/createpostbutton';
import Header from '../components/common/header'
import PostList from '../components/post/posts'
import MyProfileInfo from '../components/profile/myprofileinfo';
import { Post } from '../components/post/posts';
import { useState } from 'react';
import { useSelector } from 'react-redux';
import { selectTokenExists, selectCurrentUser } from '../features/auth/authSlice';

  
const MyProfilePage = () => {
    const [posts, setPosts] = useState<Post[]>([]); 
    const [postRatings, setPostRatings] = useState<{ postId: number; userId: number; like: boolean; dislike: boolean; }[]>([]);
    const tokenExists = useSelector(selectTokenExists);
    const user_Id = useSelector(selectCurrentUser)
    const [err, setErr] = useState(false);
    
    const handlePostsError = () => {
      setErr(true);
    };

    const changePostsError = () => {
      setErr(false)
    }

    return ( 
      <>
        <Header />
        {user_Id !== null ? (
          <>
            <MyProfileInfo userId={user_Id}/>
            <CreatePost userId={user_Id} changePostsError={changePostsError} setPosts={setPosts} setPostRatings={setPostRatings}/>
            <PostList posts={posts} err={err} handlePostsError={handlePostsError} postRatings={postRatings} setPosts={setPosts} setPostRatings={setPostRatings} tokenExists={tokenExists} auth_user_id={user_Id} sortById={true} idToSort={user_Id}/>
          </>
        ) : null}
      </>
      );
    }
    
export default MyProfilePage;