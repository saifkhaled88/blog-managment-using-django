from rest_framework import serializers
from .models import Users, Blogs, BlogCategories, Comments, Categories
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password, check_password

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['user_id', 'username', 'email', 'role', 'created_at']
        read_only_fields = ['user_id', 'created_at']



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 50)
    password = serializers.CharField(max_length = 255)

    def validate(self,data):
        
        username = data.get("username")
        password = data.get("password")
        
        try:
            user = Users.objects.get(username=username)
        except Users.DoesNotExist:
                raise serializers.ValidationError("Invalid username or password")
        

        if not check_password(password, user.password):  
            raise serializers.ValidationError("Invalid username or password.")
    
        return {"user": user}

    def create(self, validated_data):
        user = validated_data["user"]

        refresh = RefreshToken.for_user(user)
        refresh["user_id"] = user.user_id
        return {
            "user_id": user.user_id,  # Ensure you return user_id
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length = 255)

    class Meta:
        model = Users
        fields = ['username', 'password', 'password2','email', 'role']

    def validate(self,data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError("Passwords do not match!")
        return data
    

    def create(self,validated_data):
        validated_data.pop('password2')

        username = validated_data.get('username')
        if not username:
            raise serializers.ValidationError("Username is required.")
        
        password = validated_data.get('password')
        if not password:
            raise serializers.ValidationError("Password is required.")

        user = Users.objects.create(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            role=validated_data.get('role'),
            password=make_password(validated_data.get('password')) 
        )
        return user
    

class BlogsSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'  # Use the correct field for the user's representation
    )
    created_at = serializers.DateTimeField(read_only=True)

    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(),
        slug_field='name',  
    )

    class Meta:
        model = Blogs
        fields = ['blog_id','title', 'content','user', 'created_at', 'category']


class BlogCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategories
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'  # Use the correct field for the user's representation
    )
    class Meta:
        model = Comments
        fields = ['comment_id','content', 'created_at','user']


