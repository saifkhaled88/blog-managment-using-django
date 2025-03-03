from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import LoginSerializer, RegisterSerializer, BlogsSerializer,CategoriesSerializer, CommentsSerializer, UsersSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Blogs, Categories, Comments, Users
from .permissions import IsAuthor
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404




class LoginView(APIView):
    def post(self,request):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            tokens = serializer.create(serializer.validated_data)
            return Response(tokens,status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({ "message" :"Registration is completed successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BlogListView(generics.ListAPIView):
    queryset = Blogs.objects.all()
    serializer_class = BlogsSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]  # Ensure JWT is used
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['user']  # filtering by user
    search_fields = ['title']  # searching by title


class BlogCreateView(generics.CreateAPIView):
    queryset = Blogs.objects.all()
    serializer_class = BlogsSerializer
    permission_classes = [IsAuthenticated, IsAuthor]
    authentication_classes = [JWTAuthentication]  

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            raise PermissionDenied("User is not authenticated")
  


class BlogUpdateView(generics.UpdateAPIView):
    serializer_class = BlogsSerializer
    permission_classes = [IsAuthenticated, IsAuthor]
    authentication_classes = [JWTAuthentication] 
    lookup_field = 'blog_id'

    def get_queryset(self):
        return Blogs.objects.filter(user = self.request.user)
    


class BlogDeleteView(generics.DestroyAPIView):
    serializer_class = BlogsSerializer
    permission_classes = [IsAuthenticated, IsAuthor]
    authentication_classes = [JWTAuthentication] 
    lookup_field = 'blog_id'

    def get_queryset(self):
        return Blogs.objects.filter(user = self.request.user)

class BlogDetailView(generics.RetrieveAPIView):
    queryset = Blogs.objects.all()
    serializer_class = BlogsSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]  
    lookup_field = 'blog_id'



class CategoryListView(generics.ListAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication] 


class CategoryDetailListView(generics.RetrieveAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]  
    lookup_field = 'category_id'


class CommentsListView(generics.ListAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication] 
    lookup_field = 'comment_id'

    def get_queryset(self):
        comment_id = self.kwargs.get("comment_id")
        return Comments.objects.filter(comment_id=comment_id)
        

class CommentsCreateView(generics.CreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        blog_id = self.kwargs.get('blog_id')
        blog = get_object_or_404(Blogs, blog_id=blog_id)  # fetch the blog
        serializer.save(blog=blog, user=self.request.user) # Ensure the user is saved


class CommentsUpdateView(generics.UpdateAPIView):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


    def get_object(self):
        blog_id = self.kwargs.get('blog_id')
        comment_id = self.kwargs.get('comment_id')
        return get_object_or_404(Comments, blog_id=blog_id, comment_id=comment_id, user=self.request.user)


class CommentsDeleteView(generics.DestroyAPIView):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        blog_id = self.kwargs.get('blog_id')
        comment_id = self.kwargs.get('comment_id')
        return get_object_or_404(Comments,blog_id = blog_id, comment_id = comment_id,user = self.request.user)


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]  
    lookup_field = 'user_id'

    def get_object(self):
        # Get the current authenticated user ID
        return get_object_or_404(Users, user_id=self.request.user.user_id)
    

class UserProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]  

    def get_object(self):
        return self.request.user


class UserBlogsListView(generics.ListAPIView):
    serializer_class = BlogsSerializer
    permission_classes = [IsAuthenticated,IsAuthor]
    authentication_classes = [JWTAuthentication] 

    def get_queryset(self):
        return Blogs.objects.filter(user = self.request.user)


class UserCommentsListView(generics.ListAPIView):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]  

    def get_queryset(self):
        return Comments.objects.filter(user=self.request.user)
