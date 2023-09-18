import Header from '../components/common/header'
import PostList from '../components/post/posts'
import { useParams } from 'react-router-dom';
import ProfileInfo from '../components/profile/profileinfo';
import { useState } from 'react';
import { Post } from '../components/post/posts';  
import { useSelector } from 'react-redux';
import { selectTokenExists, selectCurrentUser } from '../features/auth/authSlice';
import MyProfileInfo from '../components/profile/myprofileinfo';
import CreatePost from '../components/post/createpostbutton';

  
const ProfilePage = () => {
    const { user_id } = useParams<{ user_id: string }>();
    const [profileError, setProfileError] = useState(false);
    const [posts, setPosts] = useState<Post[]>([]); 
    const [postRatings, setPostRatings] = useState<{ postId: number; userId: number; like: boolean; dislike: boolean; }[]>([]);
    const tokenExists = useSelector(selectTokenExists);
    const userId = useSelector(selectCurrentUser)
    const [err, setErr] = useState(false);

    const handleProfileError = () => {
      setProfileError(true);
    };
   
    const handlePostsError = () => {
      setErr(true);
    };

    const changePostsError = () => {
      setErr(false)
    }


    return (
      <>
      {Number(user_id) === userId ? (
          <>
            <Header />
            <MyProfileInfo userId={userId}/>
            <CreatePost userId={userId} changePostsError={changePostsError} setPosts={setPosts} setPostRatings={setPostRatings}/>
            <PostList posts={posts} err={err} handlePostsError={handlePostsError} postRatings={postRatings} setPosts={setPosts} setPostRatings={setPostRatings} tokenExists={tokenExists} auth_user_id={userId} sortById={true} idToSort={userId}/>
          </>

       ) : (
        <>
          <Header />
          <ProfileInfo userId={Number(user_id)} onError={handleProfileError} />
          {!profileError && <PostList posts={posts} err={err} handlePostsError={handlePostsError} postRatings={postRatings} setPosts={setPosts} setPostRatings={setPostRatings} tokenExists={tokenExists} auth_user_id={userId} sortById={true} idToSort={Number(user_id)} />}
        </>
       )
    }
    </>
  )
}

export default ProfilePage;