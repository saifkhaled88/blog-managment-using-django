from django.urls import path
from .views import LoginView, RegisterView, BlogListView, BlogCreateView, BlogUpdateView, BlogDeleteView, BlogDetailView, CommentsListView,CommentsCreateView,CommentsUpdateView,CommentsDeleteView,CommentDetailView, CategoryListView, CategoryDetailListView, UserProfileView, UserProfileUpdateView ,UserBlogsListView, UserCommentsListView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # JWT Urls
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Login and Registration Urls
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),

    # Blogs CRUD
    path('blogs/', BlogListView.as_view(), name='blogs'),  #done
    path('blog-create/', BlogCreateView.as_view(), name='blog-create'), #done
    path('blog-update/<int:blog_id>/', BlogUpdateView.as_view(), name='blog-update'), #done
    path('blog-delete/<int:blog_id>/', BlogDeleteView.as_view(), name='blog-delete'), #done
    path('blog-detail/<int:blog_id>/', BlogDetailView.as_view(), name='blog-detail'), #done
    
    #Category CRUD
    path('categories/', CategoryListView.as_view(), name='categories'), #done
    path('categories-detail/<int:category_id>/', CategoryDetailListView.as_view(), name='categories-detail'), #done

    # Comments CRUD
    path('comments/', CommentsListView.as_view(), name='comments'),
    path('comment-create/<int:blog_id>/', CommentsCreateView.as_view(), name='comment-create'), #done
    path('comment-update/<int:blog_id>/<int:comment_id>/', CommentsUpdateView.as_view(), name='comment-update'), #done
    path('comment-delete/<int:blog_id>/<int:comment_id>/', CommentsDeleteView.as_view(), name='comment-delete'), #done
    path('comment-detail/<int:comment_id>/', CommentDetailView.as_view(), name='comment-detail'), #done

    
    #User CRUD
    path('user-profile/', UserProfileView.as_view(), name='user-profile'), #done
    path('user-profile/update/', UserProfileUpdateView.as_view(), name='user-profile-update'), #done
    path('user-blogs/', UserBlogsListView.as_view(), name='user-blogs'), #done
    path('user-comments/', UserCommentsListView.as_view(), name='user-comments'), #done


]