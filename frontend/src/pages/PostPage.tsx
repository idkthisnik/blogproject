import Header from '../components/common/header'
import { useParams } from 'react-router-dom';
import OnePost from '../components/post/post';
import CommentsList from '../components/comment/comments';
import { useSelector } from 'react-redux';
import { selectCurrentUser } from '../features/auth/authSlice'; 
import { useState } from 'react';
import PostDeletedPage from '../components/post/postdeleted';


const PostPage = () => {
    const { post_id } = useParams<{ post_id: string }>()
    const userId = useSelector(selectCurrentUser)
    const [profileError, setProfileError] = useState(true);
    const [postDeleted, setPostDeleted] = useState(false)
    
    const handleProfileError = () => {
      setProfileError(prev => !prev);
    };

    return ( 
        <>
          <Header />
            {postDeleted === false && userId !== null ? (
              <>   
                <OnePost user_id={userId} post_id={Number(post_id)} onError={handleProfileError} setPostDeleted={setPostDeleted}/>
                {!profileError && <CommentsList user_id={userId} post_id={Number(post_id)} />}
              </>
            ) : 
              <>
                <PostDeletedPage />
              </>
            }    
        </>
    );
}
    
export default PostPage;